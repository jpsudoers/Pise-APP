import os
import dj_database_url

# Asegúrate de que ROOT_URLCONF apunte correctamente
ROOT_URLCONF = 'pise_app.urls'

# Y también el WSGI_APPLICATION
WSGI_APPLICATION = 'pise_app.wsgi.application' 