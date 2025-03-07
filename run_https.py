#!/usr/bin/env python
"""Script para ejecutar el servidor Django con soporte HTTPS"""
import os
import sys
import subprocess
import signal
import traceback

# Aseguramos que DEBUG esté activado para ver errores detallados
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docmanager.settings')
os.environ['DEBUG'] = 'True'

# Generar certificados SSL si no existen
if not (os.path.exists('cert.crt') and os.path.exists('cert.key')):
    print("Generando certificados SSL autoifirmados...")
    subprocess.run(
        'openssl req -x509 -newkey rsa:4096 -nodes -out cert.crt -keyout cert.key '
        '-days 365 -subj "/CN=localhost"',
        shell=True, check=True
    )
    print("Certificados generados correctamente.")

# Importamos luego de generar los certificados para no detener la ejecución si faltan dependencias
try:
    from werkzeug.serving import run_simple
    from django.core.wsgi import get_wsgi_application
except ImportError:
    print("Instalando dependencias necesarias...")
    subprocess.run('pip install werkzeug', shell=True, check=True)
    from werkzeug.serving import run_simple
    from django.core.wsgi import get_wsgi_application

# Verificar si la base de datos está migrada
try:
    import django
    django.setup()
    from django.db import connection
    connection.cursor()
    print("✅ Conexión a la base de datos verificada")
except Exception as e:
    print("❌ Error de base de datos detectado:")
    print(e)
    print("\nEs posible que necesites aplicar las migraciones:")
    print("python manage.py migrate")
    print("\n¿Deseas ejecutar las migraciones ahora? (s/n)")
    response = input().lower()
    if response == 's':
        try:
            subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
            print("✅ Migraciones aplicadas correctamente")
        except subprocess.CalledProcessError:
            print("❌ Error al aplicar migraciones")
            sys.exit(1)

# Configurar entorno Django
try:
    application = get_wsgi_application()
    print("✅ Aplicación Django cargada correctamente")
except Exception as e:
    print("❌ Error al cargar la aplicación Django:")
    print(e)
    traceback.print_exc()
    sys.exit(1)

# Puerto predeterminado
DEFAULT_PORT = 8000

def signal_handler(sig, frame):
    print('\nServidor detenido')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Puerto inválido: {sys.argv[1]}. Usando puerto predeterminado: {DEFAULT_PORT}")
    
    print(f"Ejecutando servidor HTTPS en https://127.0.0.1:{port}/")
    print("La primera vez que accedas, verás una advertencia de seguridad. Esto es normal.")
    print("Puedes hacer clic en 'Avanzado' y luego 'Proceder a localhost (no seguro)'.")
    print("Presiona Ctrl+C para detener el servidor.")
    
    # Configuramos werkzeug para mostrar errores completos
    run_simple('127.0.0.1', port, application,
               ssl_context=('cert.crt', 'cert.key'),
               use_reloader=True, use_debugger=True, use_evalex=True) 