#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Creando estructura de directorios..."
mkdir -p pise_app
touch pise_app/__init__.py
mv settings.py urls.py wsgi.py pise_app/

echo "Contenido del directorio actual:"
ls -la

echo "Estructura del proyecto:"
find . -type f -name "*.py"

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate 