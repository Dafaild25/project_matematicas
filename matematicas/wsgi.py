"""
WSGI config for matematicas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matematicas.settings.prod')

try:
    application = get_wsgi_application()
except Exception as e:
    sys.stderr.write(f"WSGI failed: {e}\n")
    raise
