from .base import *
import dj_database_url
import os

DEBUG = False

ALLOWED_HOSTS = ["*"]  # O el dominio de Railway si lo tienes

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# Archivos estáticos (usa el mismo BASE_DIR importado desde base.py)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}