#!/usr/bin/env bash
echo "Listing directory contents..."
ls -la
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input --clear
python manage.py migrate 