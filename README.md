# TGA Chat Generator

Aplicación web desarrollada con FastAPI para generar chats personalizados.

## 🚀 Características

- Interfaz web moderna y responsiva
- Servidor rápido con FastAPI
- Fácil de configurar y desplegar

## 🛠️ Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/tga_chat_generator.git
   cd tga_chat_generator
   ```

2. **Crear y activar entorno virtual**
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

1. **Activar el entorno virtual** (si no está activado)
   ```bash
   # En macOS/Linux
   source venv/bin/activate

   # En Windows
   # .\venv\Scripts\activate
   ```

2. **Iniciar el servidor de desarrollo**
   ```bash
   uvicorn main:app --reload
   ```

3. **Abrir en el navegador**
   Abre tu navegador y visita:
   ```
   http://127.0.0.1:8000
   ```

## 📁 Estructura del proyecto

```
tga_chat_generator/
├── static/           # Archivos estáticos (CSS, JS, imágenes)
├── templates/        # Plantillas HTML
│   └── index.html    # Página principal
├── main.py           # Aplicación principal de FastAPI
├── requirements.txt  # Dependencias del proyecto
└── README.md         # Este archivo
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
