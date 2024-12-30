#!/usr/bin/env bash
# Crear archivo build.sh en la raíz del proyecto
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate 