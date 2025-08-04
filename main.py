from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
from pathlib import Path
import logging
import os
from src.browser_screenshot import ScreenshotTaker, DeviceType

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

# Configurar directorio estático
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
    full_path = os.path.join("static", file_path)
    exists = os.path.exists(full_path)
    return {
        "file_path": file_path,
        "full_path": os.path.abspath(full_path),
        "exists": exists,
        "is_file": exists and os.path.isfile(full_path),
        "files_in_static": os.listdir("static") if os.path.exists("static") else "No existe el directorio static"
    }

# Ruta principal que sirve el index.html
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint para capturar capturas de pantalla
@app.post("/api/screenshot")
async def take_screenshot(http_request: Request):
    try:
        # Crear directorio de capturas si no existe
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)
        
        # Generar un nombre de archivo único con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.jpg"
        output_path = screenshots_dir / filename
        
        # Obtener la URL base del servidor actual
        base_url = str(http_request.base_url)
        if base_url.endswith('/'):
            base_url = base_url[:-1]  # Eliminar la barra final si existe

        # Usar el nuevo ScreenshotTaker con configuración mejorada de calidad
        async with ScreenshotTaker(headless=True) as st:
            await st.capture(
                url=base_url,
                output_path=str(output_path),
                device_type=DeviceType.IPHONE_13_PRO,
                zoom_level=2.5,
                quality=100,
                wait_for_load=True,
                wait_after_load=2000
            )
        
        # Devolver la URL relativa para acceder a la captura
        return {
            "status": "success",
            "screenshot_url": f"{base_url}/screenshots/{filename}",
            "saved_path": str(output_path)
        }
        
    except Exception as e:
        logger.error(f"Error al capturar la pantalla: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Servir las capturas de pantalla
@app.get("/screenshots/{filename}")
async def get_screenshot(filename: str):
    file_path = Path("screenshots") / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Captura no encontrada")
    return FileResponse(file_path)

if __name__ == "__main__":
    # Ejecutar el servidor
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)