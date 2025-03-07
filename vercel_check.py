#!/usr/bin/env python
"""
Script para verificar la configuración de Vercel antes del despliegue
"""
import os
import sys
import json

def check_vercel_json():
    """Verifica la configuración de vercel.json"""
    print("Verificando vercel.json...")
    
    if not os.path.exists('vercel.json'):
        print("❌ Error: vercel.json no encontrado")
        return False
    
    try:
        with open('vercel.json', 'r') as f:
            config = json.load(f)
        
        # Verificar estructura básica
        if 'builds' not in config:
            print("❌ Error: 'builds' no encontrado en vercel.json")
            return False
        
        if 'routes' not in config:
            print("❌ Error: 'routes' no encontrado en vercel.json")
            return False
        
        # Verificar configuración de Python
        python_build = None
        for build in config['builds']:
            if build.get('use') == '@vercel/python':
                python_build = build
                break
        
        if not python_build:
            print("❌ Error: configuración de Python no encontrada en vercel.json")
            return False
        
        if 'config' not in python_build or 'runtime' not in python_build['config']:
            print("⚠️ Advertencia: 'runtime' no especificado para Python")
        
        # Verificar configuración de archivos estáticos
        static_build = None
        for build in config['builds']:
            if build.get('src') == 'build_files.sh':
                static_build = build
                break
        
        if not static_build:
            print("❌ Error: configuración de build_files.sh no encontrada")
            return False
        
        # Verificar rutas estáticas
        static_route = False
        for route in config['routes']:
            if route.get('src', '').startswith('/static/'):
                static_route = True
                break
        
        if not static_route:
            print("⚠️ Advertencia: no se encontró ruta para archivos estáticos")
        
        print("✅ vercel.json parece estar correctamente configurado")
        return True
    
    except json.JSONDecodeError:
        print("❌ Error: vercel.json no es un JSON válido")
        return False
    except Exception as e:
        print(f"❌ Error al verificar vercel.json: {e}")
        return False

def check_build_script():
    """Verifica el script build_files.sh"""
    print("\nVerificando build_files.sh...")
    
    if not os.path.exists('build_files.sh'):
        print("❌ Error: build_files.sh no encontrado")
        return False
    
    try:
        with open('build_files.sh', 'r') as f:
            script = f.read()
        
        if 'collectstatic' not in script:
            print("❌ Error: comando collectstatic no encontrado en build_files.sh")
            return False
        
        if 'mkdir -p staticfiles' not in script:
            print("⚠️ Advertencia: no se crea el directorio staticfiles en build_files.sh")
        
        # Verificar si se usa python3 o si hay manejo de diferentes versiones
        if 'python3' not in script and 'PYTHON_CMD=' not in script:
            print("⚠️ Advertencia: no se usa python3 o no hay detección de versión de Python")
        
        print("✅ build_files.sh parece estar correctamente configurado")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar build_files.sh: {e}")
        return False

def check_requirements():
    """Verifica requirements.txt"""
    print("\nVerificando requirements.txt...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ Error: requirements.txt no encontrado")
        return False
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        required_packages = ['django', 'whitenoise', 'gunicorn']
        missing = []
        
        for package in required_packages:
            if package.lower() not in requirements.lower():
                missing.append(package)
        
        if missing:
            print(f"❌ Error: los siguientes paquetes requeridos no están en requirements.txt: {', '.join(missing)}")
            return False
        
        print("✅ requirements.txt incluye los paquetes esenciales")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar requirements.txt: {e}")
        return False

def check_wsgi():
    """Verifica la configuración de WSGI"""
    print("\nVerificando configuración WSGI...")
    
    wsgi_path = 'docmanager/wsgi.py'
    if not os.path.exists(wsgi_path):
        print(f"❌ Error: {wsgi_path} no encontrado")
        return False
    
    try:
        with open(wsgi_path, 'r') as f:
            wsgi = f.read()
        
        if 'app = application' not in wsgi:
            print("❌ Error: 'app = application' no encontrado en wsgi.py (requerido por Vercel)")
            return False
        
        print("✅ Configuración WSGI correcta para Vercel")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar wsgi.py: {e}")
        return False

def check_settings():
    """Verifica la configuración de Django settings"""
    print("\nVerificando configuración de Django...")
    
    settings_path = 'docmanager/settings.py'
    if not os.path.exists(settings_path):
        print(f"❌ Error: {settings_path} no encontrado")
        return False
    
    try:
        with open(settings_path, 'r') as f:
            settings = f.read()
        
        # Verificar dominio de Vercel en ALLOWED_HOSTS
        if '.vercel.app' not in settings:
            print("⚠️ Advertencia: dominio .vercel.app no incluido en ALLOWED_HOSTS")
        
        # Verificar WhiteNoise
        if 'whitenoise' not in settings:
            print("❌ Error: WhiteNoise no configurado en MIDDLEWARE")
            return False
        
        # Verificar configuración de archivos estáticos
        if 'STATIC_ROOT' not in settings:
            print("❌ Error: STATIC_ROOT no configurado")
            return False
        
        print("✅ Configuración de Django parece correcta para Vercel")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar settings.py: {e}")
        return False

def main():
    """Función principal"""
    print("=== VERIFICACIÓN DE CONFIGURACIÓN PARA VERCEL ===\n")
    
    vercel_json_ok = check_vercel_json()
    build_script_ok = check_build_script()
    requirements_ok = check_requirements()
    wsgi_ok = check_wsgi()
    settings_ok = check_settings()
    
    print("\n=== RESUMEN ===")
    print(f"vercel.json: {'✅' if vercel_json_ok else '❌'}")
    print(f"build_files.sh: {'✅' if build_script_ok else '❌'}")
    print(f"requirements.txt: {'✅' if requirements_ok else '❌'}")
    print(f"wsgi.py: {'✅' if wsgi_ok else '❌'}")
    print(f"settings.py: {'✅' if settings_ok else '❌'}")
    
    if all([vercel_json_ok, build_script_ok, requirements_ok, wsgi_ok, settings_ok]):
        print("\n✅ TODO CORRECTO - Tu proyecto parece estar listo para desplegar en Vercel! 🚀")
        return 0
    else:
        print("\n⚠️ HAY PROBLEMAS - Corrige los errores antes de desplegar en Vercel.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 