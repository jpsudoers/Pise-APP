import os
import dj_database_url

# Configuración básica
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # tus apps aquí
]

DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []
if not DEBUG:
    ALLOWED_HOSTS.extend(
        ['pise_app.onrender.com', '.render.com', 'localhost', '127.0.0.1']
    )

# Configuración de Base de datos
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600
        )
    }

# Configuración de archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Configuración de seguridad
SECRET_KEY = os.getenv('SECRET_KEY', 'tu-clave-secreta-por-defecto')

MIDDLEWARE = [
    # ... otros middleware ...
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Agregar esto para archivos estáticos
]

# Configuración de WhiteNoise para archivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Asegúrate de que ROOT_URLCONF apunte correctamente
ROOT_URLCONF = 'PISE_APP.urls'

# Y también el WSGI_APPLICATION
WSGI_APPLICATION = 'PISE_APP.wsgi.application' 