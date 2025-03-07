# Despliegue Manual en Vercel

Si has tenido problemas con el despliegue automático en Vercel, este documento proporciona instrucciones paso a paso para un despliegue manual.

## Preparación Previa

1. Asegúrate de tener instalado el CLI de Vercel:
   ```bash
   npm install -g vercel
   ```

2. Inicia sesión en tu cuenta de Vercel:
   ```bash
   vercel login
   ```

## Despliegue Manual

### Opción 1: Despliegue directo desde CLI

1. Navega a la raíz de tu proyecto:
   ```bash
   cd ruta/a/tu/proyecto
   ```

2. Ejecuta el comando de despliegue:
   ```bash
   vercel deploy --prod
   ```

3. Sigue las instrucciones en pantalla para configurar tu proyecto.

### Opción 2: Despliegue desde UI de Vercel

1. Crea un archivo `.vercel.json` en la raíz de tu proyecto con el siguiente contenido:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "build_files.sh",
         "use": "@vercel/static-build",
         "config": {
           "distDir": "staticfiles"
         }
       },
       {
         "src": "docmanager/wsgi.py",
         "use": "@vercel/python",
         "config": {
           "maxLambdaSize": "15mb",
           "runtime": "python3.9"
         }
       }
     ],
     "routes": [
       {
         "src": "/static/(.*)",
         "dest": "staticfiles/$1"
       },
       {
         "src": "/(.*)",
         "dest": "docmanager/wsgi.py"
       }
     ]
   }
   ```

2. Asegúrate de que tu `build_files.sh` esté configurado para crear archivos estáticos sin depender de Django:
   ```bash
   #!/bin/bash
   # Crear directorios
   mkdir -p staticfiles/css
   mkdir -p staticfiles/js
   
   # Crear un archivo CSS mínimo
   echo "/* Placeholder CSS */" > staticfiles/css/main.css
   
   # Copiar archivos estáticos si existen
   if [ -d "static" ]; then
       cp -r static/* staticfiles/ 2>/dev/null || true
   fi
   
   # Asignar permisos
   chmod -R 755 staticfiles
   ```

3. Añade las siguientes variables de entorno en el panel de Vercel:
   - `SECRET_KEY`: Una clave segura y aleatoria
   - `DEBUG`: false
   - `ALLOWED_HOSTS`: .vercel.app,localhost,127.0.0.1

4. Desde la interfaz de Vercel, importa tu repositorio y configura:
   - Framework Preset: Other
   - Build Command: (dejar en blanco)
   - Output Directory: staticfiles

## Solución de Problemas Comunes

### Error: "No module named 'django'"

Este error ocurre cuando las dependencias no se instalan correctamente. Soluciones:

1. Asegúrate de que `requirements.txt` esté en la raíz del proyecto
2. Verifica que el archivo tenga el formato correcto sin caracteres especiales
3. Intenta simplificar `requirements.txt` incluyendo solo django y sus dependencias esenciales

### Error: "The Output Directory staticfiles is empty"

Este error ocurre cuando el directorio de salida está vacío. Soluciones:

1. Asegúrate de que `build_files.sh` crea el directorio `staticfiles` y añade al menos un archivo
2. Verifica que el script tiene permisos de ejecución (`chmod +x build_files.sh`)
3. Prueba con un script simplificado que solo cree archivos estáticos básicos sin depender de Django

### Error: "Build Failed"

Si el build falla sin un error específico:

1. Revisa los logs completos en Vercel para identificar el punto exacto del fallo
2. Verifica que todos los archivos de configuración (`vercel.json`, `build_files.sh`, etc.) tienen el formato correcto
3. Prueba con una configuración mínima y ve añadiendo complejidad gradualmente

## Referencias

- [Documentación oficial de Vercel para Python](https://vercel.com/docs/frameworks/python)
- [Guía de Vercel para Django](https://vercel.com/guides/deploying-django-to-vercel)
- [Buenas prácticas para deployar Django](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/) 