from .base import *
import dj_database_url
import os
from pathlib import Path

DEBUG = False

# Añadir esto para permitir que Railway acceda
ALLOWED_HOSTS = ["*"]  # O mejor: ["projectmatematicas-production.up.railway.app"]

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# Archivos estáticos
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Recolectar archivos estáticos en producción
# Asegúrate de haber ejecutado `python manage.py collectstatic`
