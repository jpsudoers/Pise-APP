#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Contenido del directorio actual:"
ls -la

echo "Estructura del proyecto:"
find . -type f -name "*.py"

pip install -r requirements.txt

# Asegurarse de que el directorio static existe
mkdir -p static

python manage.py collectstatic --no-input
python manage.py migrate 