"""
WSGI config for docmanager project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docmanager.settings')

application = get_wsgi_application()

# Esta línea específica es importante para Vercel
app = application 