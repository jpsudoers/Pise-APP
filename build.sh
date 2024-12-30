#!/usr/bin/env bash
# exit on error
set -o errexit

# Crear Procfile correcto (sin espacios extras y con formato Unix)
printf "web: gunicorn config.wsgi:application --log-file -\n" > Procfile

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Creando directorios necesarios..."
mkdir -p static staticfiles media

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --no-input

echo "Creando migraciones..."
python manage.py makemigrations

echo "Ejecutando migraciones..."
python manage.py migrate

# Mostrar contenido del Procfile para verificar
echo "Contenido del Procfile:"
cat Procfile 