#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Actualizando pip..."
python -m pip install --upgrade pip

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Creando directorios necesarios..."
mkdir -p static staticfiles media

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --no-input --noinput

echo "Creando migraciones..."
python manage.py makemigrations --noinput

echo "Ejecutando migraciones..."
python manage.py migrate --noinput

# Crear Procfile
echo "web: gunicorn config.wsgi:application --bind 0.0.0.0:\$PORT" > Procfile

echo "Contenido del Procfile:"
cat Procfile 