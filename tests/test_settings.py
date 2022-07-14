""" Tests Settings
"""

import os

from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

SECRET_KEY = "fake-key"

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    # Extra apps
    "defender",
    "tz_detect",
    "menu",
    # Local apps
    "core_main_app",
    "tests",
]

# SERVER URI
SERVER_URI = "http://127.0.0.1:8000"

# TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": os.environ["POSTGRES_HOST"] if "POSTGRES_HOST" in os.environ else None,
        "PORT": int(os.environ["POSTGRES_PORT"])
        if "POSTGRES_PORT" in os.environ
        else 5432,
        "NAME": os.environ["POSTGRES_DB"] if "POSTGRES_DB" in os.environ else None,
        "USER": os.environ["POSTGRES_USER"] if "POSTGRES_USER" in os.environ else None,
        "PASSWORD": os.environ["POSTGRES_PASS"]
        if "POSTGRES_PASS" in os.environ
        else None,
    }
}

MIDDLEWARE = (
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "tz_detect.middleware.TimezoneMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core_main_app.utils.custom_context_processors.domain_context_processor",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

LOGIN_URL = "/login"
STATIC_URL = "/static/"
ROOT_URLCONF = "tests.urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
MEDIA_ROOT = "tests_media"

PASSWORD_HASHERS = ("django.contrib.auth.hashers.UnsaltedMD5PasswordHasher",)


DATA_SORTING_FIELDS = ["+title"]

CUSTOM_NAME = "Curator"
ENABLE_SAML2_SSO_AUTH = False
VERIFY_DATA_ACCESS = False

USE_TZ = True
CHECKSUM_ALGORITHM = "MD5"
