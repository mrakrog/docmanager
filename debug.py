#!/usr/bin/env python
"""
Script de diagnóstico para identificar problemas en el proyecto Django
"""
import os
import sys
import platform
import subprocess
import importlib
from pathlib import Path

def check_python():
    """Verificar la versión de Python"""
    print(f"Python versión: {platform.python_version()}")
    print(f"Python ejecutable: {sys.executable}")
    print(f"Sistema operativo: {platform.platform()}")
    
def check_django():
    """Verificar la instalación de Django"""
    try:
        import django
        print(f"Django versión: {django.get_version()}")
        
        # Verificar si se puede importar el proyecto
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docmanager.settings')
        try:
            django.setup()
            print("✅ Django setup exitoso")
        except Exception as e:
            print(f"❌ Error en django.setup(): {e}")
            return False
            
        # Verificar settings
        try:
            from django.conf import settings
            print(f"DEBUG = {settings.DEBUG}")
            print(f"ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
            print(f"STATIC_ROOT = {settings.STATIC_ROOT}")
            print(f"MEDIA_ROOT = {settings.MEDIA_ROOT}")
        except Exception as e:
            print(f"❌ Error al cargar settings: {e}")
            return False
            
        return True
    except ImportError:
        print("❌ Django no está instalado")
        return False

def check_project_structure():
    """Verificar la estructura del proyecto"""
    base_dir = Path(__file__).resolve().parent
    
    # Comprobar archivos esenciales
    essential_files = [
        "manage.py",
        "docmanager/settings.py",
        "docmanager/urls.py",
        "docmanager/wsgi.py",
    ]
    
    for file_path in essential_files:
        path = base_dir / file_path
        if path.exists():
            print(f"✅ {file_path} encontrado")
        else:
            print(f"❌ {file_path} NO encontrado")
    
    # Comprobar directorios importantes
    important_dirs = [
        "templates",
        "static",
        "media",
        "accounts",
        "docs",
    ]
    
    for dir_name in important_dirs:
        path = base_dir / dir_name
        if path.exists() and path.is_dir():
            print(f"✅ Directorio {dir_name} encontrado")
        else:
            print(f"❌ Directorio {dir_name} NO encontrado")
            # Crear si no existe
            try:
                os.makedirs(path, exist_ok=True)
                print(f"  - Directorio {dir_name} creado")
            except Exception as e:
                print(f"  - Error al crear directorio: {e}")

def check_database():
    """Verificar la base de datos"""
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docmanager.settings')
        django.setup()
        
        from django.db import connection
        
        try:
            connection.ensure_connection()
            print("✅ Conexión a la base de datos exitosa")
            
            # Verificar tablas
            cursor = connection.cursor()
            tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
            cursor.execute(tables_query)
            tables = cursor.fetchall()
            print(f"Tablas encontradas: {len(tables)}")
            for table in tables:
                print(f"  - {table[0]}")
                
            # Verificar si las migraciones están aplicadas
            try:
                from django.db.migrations.recorder import MigrationRecorder
                migrations = MigrationRecorder.Migration.objects.all()
                print(f"Migraciones aplicadas: {len(migrations)}")
                if len(migrations) == 0:
                    print("❌ No hay migraciones aplicadas. Ejecuta: python manage.py migrate")
            except Exception as e:
                print(f"❌ Error al verificar migraciones: {e}")
                
        except Exception as e:
            print(f"❌ Error de conexión a la base de datos: {e}")
            print("Recomendación: Ejecuta python manage.py migrate")
    except Exception as e:
        print(f"❌ Error al verificar base de datos: {e}")

def check_urls():
    """Verificar la configuración de URLs"""
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docmanager.settings')
        django.setup()
        
        from django.urls import get_resolver
        resolver = get_resolver()
        print(f"Total de patrones de URL: {len(resolver.url_patterns)}")
        
        print("Rutas principales:")
        for pattern in resolver.url_patterns:
            print(f"  - {pattern.pattern}")
    except Exception as e:
        print(f"❌ Error al verificar URLs: {e}")

def main():
    """Función principal"""
    print("=== DIAGNÓSTICO DEL PROYECTO DJANGO ===")
    print()
    
    print("1. Verificando Python...")
    check_python()
    print()
    
    print("2. Verificando Django...")
    django_ok = check_django()
    print()
    
    print("3. Verificando estructura del proyecto...")
    check_project_structure()
    print()
    
    if django_ok:
        print("4. Verificando base de datos...")
        check_database()
        print()
        
        print("5. Verificando URLs...")
        check_urls()
        print()
    
    print("=== RECOMENDACIONES ===")
    print("1. Asegúrate de que todas las migraciones están aplicadas:")
    print("   python manage.py migrate")
    print()
    print("2. Comprueba si hay errores en tus modelos:")
    print("   python manage.py check")
    print()
    print("3. Verifica la configuración de DEBUG en settings.py")
    print("   DEBUG = True # Para ver errores detallados")
    print()
    print("4. Usa el servidor HTTPS personalizado para depurar:")
    print("   python run_https.py")
    print()
    print("5. Intenta acceder primero a la ruta de diagnóstico:")
    print("   https://127.0.0.1:8000/health/")

if __name__ == "__main__":
    main() 