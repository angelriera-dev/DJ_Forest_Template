"""
Production environment settings.
"""

import os

from .base import *

# El componente core/security.py ya maneja DEBUG=False y otras políticas si env=prod

# Email: Backend real en producción (ejemplo SMTP)
EMAIL_BACKEND = os.environ.get(
    "DJANGO_EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)

# Logging: Menos verboso en producción, centrado en errores
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}
