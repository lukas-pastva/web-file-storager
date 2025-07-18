"""
Django settings for the “two‑package” variant
(project package: mysite, app package: web_file_storager)
"""

from pathlib import Path
import os

# ──────────────────────────────────────────────────────────────────────────────
#  CORE PATHS
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent        # /app/mysite/…

# ──────────────────────────────────────────────────────────────────────────────
#  SECURITY & DEBUG
# ──────────────────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me")  # ⚠️  nahraď v produkcii
DEBUG = False
ALLOWED_HOSTS = ["*"]

# ──────────────────────────────────────────────────────────────────────────────
#  APPLICATIONS
# ──────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "web_file_storager",          # naša doménová appka
]

# ──────────────────────────────────────────────────────────────────────────────
#  MIDDLEWARE (minimal, stačí pre read‑only appku)
# ──────────────────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

# ──────────────────────────────────────────────────────────────────────────────
#  URLCONF & WSGI/ASGI ENTRYPOINTS
# ──────────────────────────────────────────────────────────────────────────────
ROOT_URLCONF = "mysite.urls"
WSGI_APPLICATION = "mysite.wsgi.application"
ASGI_APPLICATION = "mysite.asgi.application"

# ──────────────────────────────────────────────────────────────────────────────
#  TEMPLATES
# ──────────────────────────────────────────────────────────────────────────────
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

# ──────────────────────────────────────────────────────────────────────────────
#  MEDIA – iba čítanie z /data
# ──────────────────────────────────────────────────────────────────────────────
MEDIA_DIR = Path("/data")           # volume mount: -v $(pwd)/data:/data:ro
ALLOWED_MEDIA_EXTS = {
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff",
    ".mp4", ".mov", ".m4v", ".avi", ".mkv",
}

# ──────────────────────────────────────────────────────────────────────────────
#  DATABASE – in‑memory SQLite (nič sa neukladá)
# ──────────────────────────────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("SQLITE_PATH", ":memory:"),
    }
}

# ──────────────────────────────────────────────────────────────────────────────
#  STATIC FILES (nepotrebné, no definícia zabráni warningom)
# ──────────────────────────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ──────────────────────────────────────────────────────────────────────────────
#  TIMEZONE & MISC
# ──────────────────────────────────────────────────────────────────────────────
TIME_ZONE = "UTC"
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
