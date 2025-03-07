#!/bin/bash

# Script para la construcción de archivos estáticos en Vercel
echo "Building static files..."
python manage.py collectstatic --noinput

# Asegurar que los archivos tienen permisos adecuados
chmod -R 755 staticfiles 