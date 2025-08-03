# TGA Chat Generator

Aplicación web desarrollada con FastAPI para generar chats personalizados con captura de pantalla.

## 🚀 Características

- Interfaz web moderna y responsiva
- Servidor rápido con FastAPI
- Captura de pantalla del chat generado
- Guardado automático de capturas en formato PNG/JPEG
- Apertura automática del navegador al iniciar el servidor
- Módulo de captura de pantalla programática con Playwright
- Soporte para diferentes dispositivos móviles y resoluciones
- Fácil de configurar y desplegar

## 🛠️ Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno (Chrome, Firefox, Edge, Safari)
- Playwright (se instala automáticamente con las dependencias)

## 📦 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/tga_chat_generator.git
   cd tga_chat_generator
   ```

2. **Crear y activar entorno virtual** (recomendado)
   ```bash
   # En macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # En Windows
   # python -m venv venv
   # .\venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar navegadores para Playwright**
   ```bash
   playwright install
   ```

## 🏃 Uso Básico

### Interfaz Web
1. **Iniciar el servidor**
   ```bash
   python main.py
   ```
   El servidor se iniciará en `http://localhost:8000`

2. **Abrir en el navegador**
   - Accede a `http://localhost:8000`
   - O usa: `curl http://localhost:8000/open-browser`

### Módulo de Captura Programática

El módulo `browser_screenshot.py` permite capturar páginas web programáticamente:

```python
from src.browser_screenshot import capture_webpage

# Captura una página web estándar
capture_webpage(
    url="https://ejemplo.com",
    output_path="captura.png",
    viewport_width=1920,
    viewport_height=1080,
    quality=95
)

# Captura en un dispositivo móvil específico
capture_webpage(
    url="https://ejemplo.com",
    output_path="movil.png",
    device_name='iphone_13_pro',  # Usa un perfil predefinido
    quality=95
)
```

#### Parámetros de `capture_webpage`:

- `url` (str): URL de la página a capturar
- `output_path` (str): Ruta para guardar la captura (por defecto: "screenshot.png")
- `viewport_width` (int, opcional): Ancho del viewport en píxeles
- `viewport_height` (int, opcional): Alto del viewport en píxeles
- `device_scale_factor` (float): Factor de escala para pantallas de alta densidad (por defecto: 2.0)
- `quality` (int): Calidad de la imagen (1-100) para formato JPEG
- `device_type` (str): Tipo de dispositivo ('mobile', 'tablet', 'desktop')
- `device_name` (str, opcional): Nombre del perfil de dispositivo predefinido
- `full_page` (bool): Si es True, captura toda la página desplazable
- `wait_for_load` (bool): Si es True, espera a que la red esté inactiva

#### Dispositivos predefinidos:

| Dispositivo           | Resolución  | Escala |
|-----------------------|-------------|--------|
| iPhone 13 Pro         | 390 × 844   | 3x     |
| Samsung Galaxy S21     | 360 × 800   | 3x     |
| Google Pixel 5        | 393 × 851   | 2.75x  |
| iPhone SE             | 375 × 667   | 2x     |
| iPad Air              | 1180 × 820  | 2x     |
| Samsung Galaxy Tab S7  | 800 × 1280  | 2x     |

## 🚨 Solución de problemas

### Playwright no encuentra el navegador
Si obtienes errores sobre navegadores no encontrados:
```bash
playwright install
playwright install-deps  # Solo en Linux
```

### Puerto 8000 en uso
```bash
# En macOS/Linux
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs -I {} kill -9 {}
```

## 📁 Estructura del proyecto

```
tga_chat_generator/
├── src/
│   ├── __init__.py
│   └── browser_screenshot.py  # Módulo de captura programática
├── main.py                    # Aplicación principal de FastAPI
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Este archivo
```

## 📝 Uso

1. Una vez que la aplicación se abra en tu navegador, verás la interfaz del generador de chat.
2. Personaliza el chat según tus necesidades.
3. Haz clic en el botón de captura para guardar una imagen del chat.
4. Las capturas se guardan automáticamente en la carpeta `screenshots/`.

## 🚨 Solución de problemas

### Puerto 8000 en uso
Si el puerto 8000 está en uso, puedes detener el proceso que lo está usando con:

```bash
# En macOS/Linux
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs -I {} kill -9 {}
```

### No se abre el navegador automáticamente
Si el navegador no se abre automáticamente, puedes acceder manualmente a:
```
http://localhost:8000
```

## 📁 Estructura del proyecto

```
tga_chat_generator/
├── main.py            # Aplicación principal de FastAPI
├── requirements.txt   # Dependencias del proyecto
├── static/            # Archivos estáticos (CSS, JS, imágenes)
├── templates/         # Plantillas HTML
│   └── index.html     # Plantilla principal
└── screenshots/       # Carpeta donde se guardan las capturas
```

## 🌐 Endpoints de la API

### `GET /open-browser`
Abre automáticamente el navegador predeterminado en la aplicación.

**Respuesta exitosa (200 OK):**
```json
{
  "status": "success",
  "message": "Navegador abierto exitosamente",
  "url": "http://127.0.0.1:8000"
}
```

**Ejemplo de uso con curl:**
```bash
curl http://localhost:8000/open-browser
```

### `POST /save-screenshot`
Guarda una captura de pantalla del chat.

**Parámetros (JSON):**
- `image` (string): Datos de la imagen en formato base64
- `filename` (string, opcional): Nombre personalizado para el archivo

**Respuesta exitosa (200 OK):**
```json
{
  "status": "success",
  "filename": "screenshot_20230802_123456.png",
  "path": "/ruta/completa/screenshots/screenshot_20230802_123456.png"
}
```

## 📦 Dependencias principales

- FastAPI - Framework web moderno y rápido
- Uvicorn - Servidor ASGI
- Jinja2 - Motor de plantillas
- python-multipart - Para manejar datos de formulario

```

## 🔧 Variables de entorno

Crea un archivo `.env` en la raíz del proyecto si necesitas configurar variables de entorno:

```env
# Configuración de la aplicación
APP_NAME="TGA Chat Generator"
DEBUG=True
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor, lee nuestras pautas de contribución para más detalles.

## 📧 Contacto

Tu Nombre - [@tuusuario](https://twitter.com/tuusuario)

Enlace del proyecto: [https://github.com/tu-usuario/tga_chat_generator](https://github.com/tu-usuario/tga_chat_generator)
