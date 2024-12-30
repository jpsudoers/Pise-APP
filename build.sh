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

echo "==== Estructura completa del proyecto ===="
tree -a

# Asegurarse de que el directorio static existe
mkdir -p static

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate 