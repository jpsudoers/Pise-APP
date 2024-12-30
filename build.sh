#!/usr/bin/env bash
# exit on error
set -o errexit

# Crear Procfile correcto
cat > Procfile << 'EOL'
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
EOL

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

# Verificar el contenido del Procfile
echo "Contenido del Procfile:"
cat Procfile 