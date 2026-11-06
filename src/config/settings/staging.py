# pyright: reportConstantRedefinition=false
"""Production-like settings for local or isolated staging deployments."""

from .prod import *

# Keep outbound email inert until a real staging mail integration is configured.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
