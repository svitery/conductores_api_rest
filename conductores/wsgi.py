"""
WSGI config for conductores project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

"""
Código que se ejecuta cuando inicia la aplicación, se encarga de consultar el endpoint de los datos
"""
import datos.load_database

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conductores.settings')

application = get_wsgi_application()
