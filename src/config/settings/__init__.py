"""
Django settings environment detection and loading.

Environment is determined by DJANGO_ENV environment variable.
Valid values: dev, staging, prod, local
Default: dev
"""

import os

# Environment detection
ENV = os.environ.get("DJANGO_ENV", "dev").lower()

# Valid environments
VALID_ENVIRONMENTS = {"dev", "staging", "prod", "local"}

if ENV not in VALID_ENVIRONMENTS:
    raise ValueError(
        f"Invalid DJANGO_ENV '{ENV}'. Must be one of: {', '.join(VALID_ENVIRONMENTS)}"
    )

# Environment-specific settings module
SETTINGS_MODULE = f"config.settings.{ENV}"

# Lazy settings import - actual settings are loaded by Django
# This __init__ just provides environment detection utilities
__all__ = ["ENV", "SETTINGS_MODULE"]
