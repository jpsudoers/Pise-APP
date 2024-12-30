#!/usr/bin/env bash
# exit on error
set -o errexit

# Renombrar el directorio si es necesario
if [ -d "PISE_APP" ] && [ ! -d "pise_app" ]; then
    mv PISE_APP pise_app
fi

echo "Contenido del directorio actual:"
ls -la

echo "Estructura del proyecto:"
find . -type f -name "*.py"

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate 