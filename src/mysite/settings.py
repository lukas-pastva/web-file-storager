"""
Django settings pre projekt „mysite“
(app: web_file_storager, úložisko médií: /data)
"""

from pathlib import Path
import os

# ─────────────────────────────────────────────
#  CORE PATHS
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────
#  SECURITY & DEBUG
# ─────────────────────────────────────────────
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me")   # ⚠️  nahraď v produkcii
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = ["*"]

# ─────────────────────────────────────────────
#  APPLICATIONS
# ─────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "web_file_storager",
]

# ─────────────────────────────────────────────
#  MIDDLEWARE (minimal, ale nutné)
# ─────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

# ─────────────────────────────────────────────
#  URLCONF & ENTRYPOINTS
# ─────────────────────────────────────────────
ROOT_URLCONF = "mysite.urls"
WSGI_APPLICATION = "mysite.wsgi.application"
ASGI_APPLICATION = "mysite.asgi.application"

# ─────────────────────────────────────────────
#  TEMPLATES
# ─────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    }
]

# ─────────────────────────────────────────────
#  MÉDIÁ – čítanie aj upload do /data
# ─────────────────────────────────────────────
MEDIA_DIR = Path("/data")
MEDIA_ROOT = MEDIA_DIR           # pre FileSystemStorage
MEDIA_URL  = "/media/"           # len pre DEBUG = True

ALLOWED_MEDIA_EXTS = {
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff",
    ".mp4", ".mov", ".m4v", ".avi", ".mkv",
}

# ─────────────────────────────────────────────
#  DATABASE – in‑memory SQLite
# ─────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("SQLITE_PATH", ":memory:"),
    }
}

# ─────────────────────────────────────────────
#  STATIC FILES
# ─────────────────────────────────────────────
STATIC_URL  = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ─────────────────────────────────────────────
#  GLOBALS
# ─────────────────────────────────────────────
TIME_ZONE = "UTC"
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
