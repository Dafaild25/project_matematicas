from .base import *
import os

DEBUG = True

# Para desarrollo local, siempre usar SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Configuración adicional para desarrollo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'