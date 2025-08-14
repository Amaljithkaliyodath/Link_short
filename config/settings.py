"""
Django settings for config project.
Crafted for Vercel (serverless) + SQLite by default, with env overrides.
"""

from pathlib import Path
import os
import environ

# ------------------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------------------
# Env (works even if .env is missing)
# ------------------------------------------------------------------------------
env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str, "django-insecure-change-me-please"),
    ALLOWED_HOSTS=(list, ["*"]),
    DATABASE_URL=(str, f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
    RATE_PER_MINUTE=(int, 20),
)

env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

# ------------------------------------------------------------------------------
# Core
# ------------------------------------------------------------------------------
DEBUG = env("DEBUG")
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")
RATE_PER_MINUTE = env("RATE_PER_MINUTE")

# ------------------------------------------------------------------------------
# Apps
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # project apps
    "links",
]

# ------------------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve static on Vercel
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ------------------------------------------------------------------------------
# URLs / WSGI / ASGI
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ------------------------------------------------------------------------------
# Templates
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "links" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

# ------------------------------------------------------------------------------
# Database
#   - Default: SQLite (bundled file) — fine for demo on Vercel (non-persistent)
#   - To switch to Postgres: set DATABASE_URL in Vercel env
# ------------------------------------------------------------------------------
DATABASES = {"default": env.db()}

# ------------------------------------------------------------------------------
# Static files (collect locally once, commit /static to repo)
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ------------------------------------------------------------------------------
# Security / proxies (safe defaults for serverless)
# ------------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = ["https://*"]  # broad for demo; tighten for custom domains

# ------------------------------------------------------------------------------
# Misc
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
