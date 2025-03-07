# Sistema de Gestión de Documentación

Un sistema completo para gestionar la documentación de tu empresa, con Django en el backend y Tailwind CSS en el frontend.

![Django](https://img.shields.io/badge/Django-4.2.10-green)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.3.3-blue)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)

## 📋 Características

- ✅ Autenticación de usuarios
- 📄 Gestión de documentos (subida, descarga, visualización)
- 🗂️ Categorización y etiquetado de documentos
- 🔍 Búsqueda avanzada de documentos
- 📱 Interfaz moderna y responsiva con Tailwind CSS
- 🔄 Control de versiones de documentos
- 🛡️ Permisos y accesos configurables

## 🖼️ Capturas de pantalla

_Próximamente_

## 🚀 Requisitos

- Python 3.8+
- Node.js y npm
- Git

## ⚙️ Configuración

1. Clonar el repositorio
   ```bash
   git clone https://github.com/tu-usuario/docmanager.git
   cd docmanager
   ```

2. Crear y activar entorno virtual
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias
   ```bash
   pip install -r requirements.txt
   pip install django-extensions werkzeug pyOpenSSL
   ```

4. Configurar variables de entorno
   - Copiar `.env.example` a `.env`
   - Ajustar los valores según sea necesario

5. Aplicar migraciones
   ```bash
   python manage.py migrate
   ```

6. Instalar dependencias frontend
   ```bash
   npm install
   ```

## 🏃‍♂️ Ejecutar el servidor

### Con HTTP (desarrollo estándar)
```bash
python manage.py runserver
```
Accede a: http://127.0.0.1:8000/

### Con HTTPS (recomendado)
```bash
python run_https.py
```
Accede a: https://127.0.0.1:8000/

Si deseas usar un puerto diferente:
```bash
python run_https.py 8443
```
Accede a: https://127.0.0.1:8443/

**Nota:** Al acceder por primera vez con HTTPS, verás una advertencia de seguridad. Esto es normal porque estamos usando un certificado autofirmado para desarrollo local. Haz clic en "Avanzado" y luego "Proceder a localhost (no seguro)" para continuar.

## 🌐 Despliegue en Vercel

El proyecto está configurado para ser desplegado en Vercel siguiendo la documentación oficial:
[Deploying Django to Vercel](https://vercel.com/guides/deploying-django-to-vercel)

## 🗂️ Estructura del Proyecto

- `docmanager/` - Aplicación principal Django
- `accounts/` - Gestión de usuarios y permisos
- `docs/` - Gestión de documentos
- `static/` - Archivos estáticos (CSS, JS)
- `templates/` - Plantillas HTML
- `media/` - Archivos subidos por los usuarios (documentos)

## 🧪 Diagnóstico

Si encuentras algún problema, puedes ejecutar el script de diagnóstico:
```bash
python debug.py
```

## 📜 Licencia

[MIT](LICENSE)

## 👥 Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios importantes antes de enviar un pull request. 
``` 