import os
import dj_database_url

# Configuración básica
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuración de seguridad
SECRET_KEY = os.getenv('SECRET_KEY', 'x0u)3f%0s$u##t)tz^$!jftn&t+!g)toqiwgo1jpg6%c3s4f(!')
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []
if not DEBUG:
    ALLOWED_HOSTS.extend([
        'tu-nombre-app.onrender.com',  # Reemplaza con tu dominio real de Render
        '.render.com',
        'localhost',
        '127.0.0.1'
    ])

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Tus apps
    'accounts',
    'miapp',
    'pages',
    'pise',
    'piseapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PISE_APP.urls'
WSGI_APPLICATION = 'PISE_APP.wsgi.application'

# Base de datos
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://pise:pise_2022@35.170.104.222:5432/PiseApp')
DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600
    )
}

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Archivos media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')