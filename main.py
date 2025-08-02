from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Crear la aplicación FastAPI
app = FastAPI(title="TGA Chat Generator")

# Configurar el directorio de plantillas
templates = Jinja2Templates(directory="templates")

# Montar directorio estático para archivos CSS, JS, imágenes, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ruta principal que sirve el index.html
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Si necesitas más rutas API, puedes agregarlas aquí
# @app.get("/api/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}

# Para ejecutar directamente con: python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)