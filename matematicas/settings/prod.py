from .base import *
import dj_database_url

DEBUG = False

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
