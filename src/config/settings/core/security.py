import os

env = os.environ.get("DJANGO_ENV", "dev").lower()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "django-insecure-fallback-key-for-dev-only"
)

# DEBUG se adapta al entorno
DEBUG = env != "prod"

# Hosts permitidos
if env == "prod":
    _allowed_hosts = os.environ.get("ALLOWED_HOSTS", "").split(",")
else:
    _allowed_hosts = ["*"]
ALLOWED_HOSTS = _allowed_hosts

# CSRF Trusted Origins
csrf_origins = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
if csrf_origins:
    _csrf_origins = [
        origin.strip() for origin in csrf_origins.split(",") if origin.strip()
    ]
else:
    _csrf_origins = ["http://localhost:8000", "http://127.0.0.1:8000"]
CSRF_TRUSTED_ORIGINS = _csrf_origins

# OWASP & Hardening Settings (Phase 1)
if env == "prod":
    _hsts_seconds = 31536000
    _ssl_redirect = True
    _cookie_secure = True
else:
    _hsts_seconds = 0
    _ssl_redirect = False
    _cookie_secure = False

SECURE_HSTS_SECONDS = _hsts_seconds
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = _ssl_redirect
SESSION_COOKIE_SECURE = _cookie_secure
CSRF_COOKIE_SECURE = _cookie_secure

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"
