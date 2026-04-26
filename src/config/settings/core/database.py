import os
from pathlib import Path

# Calculamos BASE_DIR aquí para evitar dependencias circulares si se importa solo,
# pero manteniendo la coherencia con base.py
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

env = os.environ.get("DJANGO_ENV", "dev").lower()

if env == "prod":
    # Configuración de Producción (PostgreSQL)
    _databases = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME"),
            "USER": os.environ.get("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASSWORD"),
            "HOST": os.environ.get("DB_HOST", "db"),
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }
else:
    # Configuración de Desarrollo/Local (SQLite)
    _databases = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
DATABASES = _databases
