from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# STATIC & MEDIA SETTINGS

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
