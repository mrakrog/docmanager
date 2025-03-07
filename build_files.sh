#!/bin/bash

# Script para la construcción de archivos estáticos en Vercel
echo "Building static files..."

# Asegurar que estamos usando la versión correcta de Python en Vercel
if command -v python3 &>/dev/null; then
    echo "Using python3..."
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    echo "Using python..."
    PYTHON_CMD=python
else
    echo "Python not found!"
    exit 1
fi

# Crear directorio staticfiles si no existe
echo "Creating staticfiles directory if it doesn't exist..."
mkdir -p staticfiles

# Recolectar archivos estáticos
echo "Collecting static files..."
$PYTHON_CMD manage.py collectstatic --noinput

# Asegurar que los archivos tienen permisos adecuados
echo "Setting permissions for staticfiles..."
chmod -R 755 staticfiles 