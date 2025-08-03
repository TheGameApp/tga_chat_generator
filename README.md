# TGA Chat Generator

Aplicación web desarrollada con FastAPI para generar chats personalizados con captura de pantalla.

## 🚀 Características

- Interfaz web moderna y responsiva
- Servidor rápido con FastAPI
- Captura de pantalla del chat generado
- Guardado automático de capturas en formato PNG
- Apertura automática del navegador al iniciar el servidor
- Fácil de configurar y desplegar

## 🛠️ Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

## 🚀 Instalación

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

## 🏃 Ejecución

1. **Activar el entorno virtual** (si se usó)
   ```bash
   # En macOS/Linux
   source venv/bin/activate

   # En Windows
   # .\venv\Scripts\activate
   ```

2. **Iniciar el servidor**
   ```bash
   python main.py
   ```
   
   El servidor se iniciará en `http://localhost:8000` y se abrirá automáticamente en tu navegador predeterminado.

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
