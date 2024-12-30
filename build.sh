#!/usr/bin/env bash
# exit on error
set -o errexit

# Crear Procfile correcto
echo "web: gunicorn config.wsgi:application --log-file -" > Procfile

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Creando directorios necesarios..."
mkdir -p static staticfiles media

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --no-input

echo "Ejecutando migraciones..."
python manage.py migrate 