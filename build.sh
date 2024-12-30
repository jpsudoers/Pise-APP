#!/usr/bin/env bash
# exit on error
set -o errexit

echo "==== Verificando estructura del proyecto ===="
# Crear directorio PISE_APP si no existe
mkdir -p PISE_APP

# Asegurarse de que existe __init__.py
touch PISE_APP/__init__.py

# Mover archivos principales si están en la raíz
for file in settings.py urls.py wsgi.py; do
    if [ -f "$file" ]; then
        echo "Moviendo $file a PISE_APP/"
        mv "$file" PISE_APP/
    fi
done

echo "==== Contenido del directorio actual ===="
ls -la

echo "==== Contenido de PISE_APP ===="
ls -la PISE_APP/

# Crear archivos necesarios si no existen
if [ ! -f "PISE_APP/urls.py" ]; then
    echo "Creando urls.py básico..."
    cat > PISE_APP/urls.py << EOL
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]
EOL
fi

if [ ! -f "PISE_APP/wsgi.py" ]; then
    echo "Creando wsgi.py básico..."
    cat > PISE_APP/wsgi.py << EOL
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PISE_APP.settings')
application = get_wsgi_application()
EOL
fi

# Crear directorios necesarios
mkdir -p static
mkdir -p staticfiles

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar comandos de Django con debug
echo "==== Ejecutando collectstatic ===="
python -v manage.py collectstatic --no-input

echo "==== Ejecutando migrate ===="
python -v manage.py migrate 