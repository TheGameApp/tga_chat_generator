# TGA Chat Generator - Guía de Instalación en Ubuntu 24.04

Esta guía te ayudará a configurar y ejecutar TGA Chat Generator en un servidor Ubuntu 24.04.

## Requisitos Previos

1. **Actualizar el sistema**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Instalar Python y herramientas esenciales**:
   ```bash
   sudo apt install -y python3 python3-pip python3-venv git
   ```

## Configuración del Entorno

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/TheGameApp/tga_chat_generator.git
   cd tga_chat_generator
   ```

2. **Crear y activar entorno virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias de Python**:
   ```bash
   pip install -r requirements.txt
   ```

## Instalación de Dependencias de Playwright

1. **Instalar dependencias del sistema**:
   ```bash
   sudo apt-get install -y \
       libnss3 \
       libatk1.0-0t64 \
       libatk-bridge2.0-0t64 \
       libcups2t64 \
       libxkbcommon0 \
       libxcomposite1 \
       libxdamage1 \
       libxfixes3 \
       libxrandr2 \
       libgbm1 \
       libpango-1.0-0 \
       libcairo2 \
       libasound2t64
   ```

2. **Instalar dependencias de Playwright**:
   ```bash
   npx playwright install-deps
   npx playwright install --with-deps chromium
   ```

3. **Solución para libvpx7** (si es necesario):
   ```bash
   # Instalar libvpx9
   sudo apt-get install -y libvpx9
   
   # Crear enlace simbólico
   sudo ln -s /usr/lib/x86_64-linux-gnu/libvpx.so.9 /usr/lib/x86_64-linux-gnu/libvpx.so.7
   ```

## Cambios en el Código

Asegúrate de que el código use Chromium en lugar de WebKit. En `src/browser_screenshot.py`:

```python
self.browser = await self.playwright.chromium.launch(
    headless=self.headless,
    args=['--disable-web-security']  # Opcional: para desarrollo local
)
```

## Ejecutar la Aplicación

1. **Iniciar el servidor**:
   ```bash
   python main.py
   ```

2. **Para ejecutar en segundo plano**:
   ```bash
   nohup python main.py > app.log 2>&1 &
   ```

3. **Verificar el estado**:
   ```bash
   tail -f app.log
   ```

## Solución de Problemas Comunes

1. **Si ves errores de dependencias faltantes**:
   ```bash
   npx playwright install-deps
   ```

2. **Si el navegador no se inicia**:
   - Verifica que todas las dependencias estén instaladas
   - Asegúrate de que el entorno virtual esté activado
   - Revisa los logs en `app.log`

3. **Para detener la aplicación**:
   ```bash
   pkill -f "python main.py"
   ```

## Configuración de Producción (Opcional)

Para un entorno de producción, considera usar un servidor WSGI como Gunicorn:

```bash
pip install gunicorn
gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 main:app
```

## Notas Importantes

- Esta configuración usa Chromium que es más estable en entornos sin interfaz gráfica
- Para entornos de producción, considera usar Docker para mayor consistencia
- Asegúrate de que el puerto 8000 esté abierto en el firewall si es necesario

## Actualizaciones

- **2024-08-04**: Documentación inicial creada para Ubuntu 24.04
- **2024-08-04**: Solución para libvpx7 agregada
- **2024-08-04**: Cambio a Chromium como navegador predeterminado
