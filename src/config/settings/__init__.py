"""Select a supported Django settings module from ``DJANGO_ENV``."""

import os

ENV = os.environ.get("DJANGO_ENV", "dev").lower()
VALID_ENVIRONMENTS = {"dev", "staging", "prod"}

if ENV not in VALID_ENVIRONMENTS:
    raise ValueError(
        f"Invalid DJANGO_ENV '{ENV}'. "
        f"Must be one of: {', '.join(sorted(VALID_ENVIRONMENTS))}"
    )

SETTINGS_MODULE = f"config.settings.{ENV}"

__all__ = ["ENV", "SETTINGS_MODULE", "VALID_ENVIRONMENTS"]
