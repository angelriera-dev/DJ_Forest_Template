"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from config.settings import SETTINGS_MODULE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MODULE)

application = get_wsgi_application()
