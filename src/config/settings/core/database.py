# pyright: reportConstantRedefinition=false
"""Database settings shared by dev, staging, and production."""

import os
from pathlib import Path
from typing import Any, cast

import environ
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


def _postgres_database() -> dict[str, Any]:
    database_url = os.environ.get("DATABASE_URL", "").strip()
    if database_url:
        database = cast(dict[str, Any], environ.Env.db_url_config(database_url))  # pyright: ignore[reportUnknownMemberType]
        required = ("NAME", "USER", "PASSWORD", "HOST")
        if database["ENGINE"] != "django.db.backends.postgresql" or any(
            not database.get(key) for key in required
        ):
            raise ImproperlyConfigured(
                "DATABASE_URL must provide PostgreSQL engine, database, "
                "credentials, and host"
            )
        if os.environ.get("DJANGO_ENV", "dev").lower() != "dev":
            options = cast(dict[str, Any], database.setdefault("OPTIONS", {}))
            sslmode = options.get("sslmode")
            if sslmode and sslmode not in {"require", "verify-ca", "verify-full"}:
                raise ImproperlyConfigured(
                    "Non-development DATABASE_URL must enable PostgreSQL TLS"
                )
            options.setdefault("sslmode", "require")
        return database

    required = ("DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise ImproperlyConfigured(
            f"Missing required database configuration: {', '.join(missing)}"
        )

    database: dict[str, Any] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
    if os.environ.get("DJANGO_ENV", "dev").lower() == "prod":
        database["OPTIONS"] = {"sslmode": "require"}
    return database


if os.environ.get("DJANGO_SETTINGS_MODULE") == "config.settings.test":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {"default": _postgres_database()}
