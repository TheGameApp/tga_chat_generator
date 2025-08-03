from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import base64
import os
import webbrowser
import threading
from datetime import datetime
from pathlib import Path
import logging

# Crear la aplicación FastAPI
app = FastAPI(title="TGA Chat Generator")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, reemplazar con los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar el directorio de plantillas
templates = Jinja2Templates(directory="templates")

# Configurar directorio estático con más opciones
app.mount(
    "/static", 
    StaticFiles(
        directory="static",
        html=True,
        check_dir=True
    ), 
    name="static"
)

# Ruta para verificar archivos estáticos
@app.get("/debug/static/{file_path:path}")
async def debug_static(file_path: str):
    import os
    full_path = os.path.join("static", file_path)
    exists = os.path.exists(full_path)
    return {
        "file_path": file_path,
        "full_path": os.path.abspath(full_path),
        "exists": exists,
        "is_file": exists and os.path.isfile(full_path),
        "files_in_static": os.listdir("static") if os.path.exists("static") else "No existe el directorio static"
    }

class ScreenshotData(BaseModel):
    image: str
    filename: str = None

# Ruta principal que sirve el index.html
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ruta para guardar capturas
@app.post("/save-screenshot")
async def save_screenshot(data: ScreenshotData):
    try:
        # Crear directorio de capturas si no existe
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)
        
        # Usar el nombre de archivo proporcionado o generar uno con timestamp
        if not data.filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        else:
            # Asegurar que el nombre del archivo sea seguro
            safe_filename = "".join(c for c in data.filename if c.isalnum() or c in ('-', '_', '.')).rstrip()
            filename = f"screenshot_{safe_filename}.png"
            
        filepath = screenshots_dir / filename
        
        # Verificar que los datos de la imagen sean válidos
        if not data.image or "," not in data.image:
            logger.error("Formato de imagen no válido")
            raise HTTPException(status_code=400, detail="Formato de imagen no válido")
            
        # Decodificar y guardar la imagen
        try:
            image_data = data.image.split(",")[1]  # Remover el prefijo 'data:image/png;base64,'
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(image_data))
                
            logger.info(f"Captura guardada exitosamente: {filename}")
            return {"status": "success", "filename": filename, "path": str(filepath.absolute())}
            
        except Exception as e:
            logger.error(f"Error al guardar la imagen: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error en save_screenshot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

class BrowserResponse(BaseModel):
    status: str
    message: str
    url: str

@app.get("/open-browser", response_model=BrowserResponse)
async def open_browser_endpoint(request: Request):
    """
    Endpoint para abrir el navegador automáticamente.
    Devuelve la URL donde se abrió el navegador.
    """
    try:
        # Construir la URL completa incluyendo el esquema y el host
        url = f"{request.url.scheme}://{request.client.host}:{request.url.port}"
        
        # Usar un hilo para no bloquear la respuesta
        def _open_browser():
            import time
            time.sleep(1)  # Pequeña pausa
            webbrowser.open(url)
            logger.info(f"Navegador abierto en {url}")
        
        threading.Thread(target=_open_browser).start()
        
        return {
            "status": "success",
            "message": "Navegador abierto exitosamente",
            "url": url
        }
        
    except Exception as e:
        logger.error(f"Error al abrir el navegador: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al abrir el navegador: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    
    # Iniciar el servidor
    print("Iniciando servidor en http://localhost:8000")
    print("Para abrir el navegador automáticamente, visita: http://localhost:8000/open-browser")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)