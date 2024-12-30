#!/usr/bin/env bash
# exit on error
set -o errexit

echo "==== Verificando y corrigiendo estructura ===="
if [ -f "settings.py" ] && [ ! -f "PISE_APP/settings.py" ]; then
    mkdir -p PISE_APP
    mv settings.py PISE_APP/
    mv urls.py PISE_APP/ 2>/dev/null || true
    mv wsgi.py PISE_APP/ 2>/dev/null || true
    touch PISE_APP/__init__.py
fi

echo "==== Contenido del directorio actual ===="
ls -la

echo "==== Contenido de PISE_APP ===="
ls -la PISE_APP/ 2>/dev/null || echo "El directorio PISE_APP no existe"

echo "==== Archivos Python en el proyecto ===="
find . -name "*.py" -type f

# Asegurarse de que el directorio static existe
mkdir -p static

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar comandos de Django
DJANGO_SETTINGS_MODULE=PISE_APP.settings python manage.py collectstatic --no-input
DJANGO_SETTINGS_MODULE=PISE_APP.settings python manage.py migrate 