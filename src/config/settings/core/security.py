# pyright: reportConstantRedefinition=false
"""Environment-aware Django security settings."""

import os

from django.core.exceptions import ImproperlyConfigured

from config.settings import ENV

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-dev-only-change-me")
_database_url = os.environ.get("DATABASE_URL", "").strip()

if ENV != "dev" and not os.environ.get("DJANGO_SECRET_KEY"):
    raise ImproperlyConfigured(f"{ENV} requires DJANGO_SECRET_KEY")
if ENV == "prod" or (ENV == "staging" and _database_url):
    if SECRET_KEY.startswith("django-insecure-") or len(SECRET_KEY) < 50:
        raise ImproperlyConfigured(
            f"{ENV} requires a non-example DJANGO_SECRET_KEY of at least 50 characters"
        )

DEBUG = ENV == "dev"

if ENV == "dev":
    ALLOWED_HOSTS = ["*"]
else:
    raw_hosts = os.environ.get("ALLOWED_HOSTS", "")
    ALLOWED_HOSTS = [host.strip() for host in raw_hosts.split(",") if host.strip()]
    if not ALLOWED_HOSTS or "*" in ALLOWED_HOSTS:
        raise ImproperlyConfigured(
            f"{ENV} requires explicit ALLOWED_HOSTS; wildcard hosts are not allowed"
        )

raw_csrf_origins = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
if ENV != "dev" and not raw_csrf_origins.strip():
    raise ImproperlyConfigured(f"{ENV} requires explicit CSRF_TRUSTED_ORIGINS")
CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in raw_csrf_origins.split(",") if origin.strip()
]
if not CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

if ENV == "prod":
    SECURE_SSL_REDIRECT = True
elif ENV == "staging":
    _ssl_redirect = os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "false").lower()
    if _ssl_redirect not in {"true", "false", "1", "0", "yes", "no", "on", "off"}:
        raise ImproperlyConfigured("DJANGO_SECURE_SSL_REDIRECT must be a boolean")
    SECURE_SSL_REDIRECT = _ssl_redirect in {"true", "1", "yes", "on"}
else:
    SECURE_SSL_REDIRECT = False
_cookie_secure = SECURE_SSL_REDIRECT
SESSION_COOKIE_SECURE = _cookie_secure
CSRF_COOKIE_SECURE = _cookie_secure

SECURE_HSTS_SECONDS = 31536000 if ENV == "prod" else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"
