from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import base64
import os
import webbrowser
from datetime import datetime
from pathlib import Path

# Crear la aplicación FastAPI
app = FastAPI(title="TGA Chat Generator")

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
        
        # Generar nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = screenshots_dir / filename
        
        # Decodificar y guardar la imagen
        image_data = data.image.split(",")[1]  # Remover el prefijo 'data:image/png;base64,'
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(image_data))
            
        return {"status": "success", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def open_browser():
    import time
    time.sleep(1)  # Esperar un momento para que el servidor se inicie
    url = "http://localhost:8000"
    webbrowser.open(url)
    print(f"Navegador abierto en {url}")

if __name__ == "__main__":
    import threading
    
    # Iniciar el navegador en un hilo separado
    threading.Thread(target=open_browser).start()
    
    # Iniciar el servidor
    print("Iniciando servidor en http://localhost:8000...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)