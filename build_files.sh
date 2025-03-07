#!/bin/bash

# Script para la construcción de archivos estáticos en Vercel
echo "Building static files..."

# Crear directorio staticfiles
echo "Creating staticfiles directory..."
mkdir -p staticfiles
mkdir -p staticfiles/css
mkdir -p staticfiles/js
mkdir -p staticfiles/images

# Crear un archivo CSS mínimo
echo "Creating minimal CSS file..."
cat > staticfiles/css/main.css << EOL
/* 
 * Placeholder CSS file
 * Creado para asegurar que el directorio static no esté vacío
 * y que Vercel pueda encontrar archivos estáticos durante el despliegue
 */

body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
               'Helvetica Neue', Arial, sans-serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #0ea5e9;
  color: white;
  border-radius: 0.25rem;
  text-decoration: none;
}

.btn:hover {
  background-color: #0284c7;
}
EOL

# Copiar archivos estáticos existentes si hay alguno
if [ -d "static" ]; then
    echo "Copying existing static files..."
    cp -r static/* staticfiles/ 2>/dev/null || echo "No static files to copy"
fi

# Asegurar que los archivos tienen permisos adecuados
echo "Setting permissions for staticfiles..."
chmod -R 755 staticfiles

echo "Static files build process completed!" 