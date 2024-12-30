#!/usr/bin/env bash
# exit on error
set -o errexit

# Crear Procfile correcto usando un método diferente
cat > Procfile << 'EOL'
web: gunicorn config.wsgi:application
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

# Verificar el contenido y formato del Procfile
echo "Contenido del Procfile:"
cat Procfile
echo "Formato del Procfile (hexdump):"
hexdump -C Procfile 