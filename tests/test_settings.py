""" Settings file to run the tests.
"""

import os

from django.conf import settings
from dotenv import load_dotenv  # noqa

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
    "menu",
    # Local apps
    "core_main_app",
    "core_parser_app",
    "core_website_app",
    "tests",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "captcha",
]

# SERVER URI
SERVER_URI = "http://127.0.0.1:8000"

# TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": os.environ.get("POSTGRES_HOST", None),
        "PORT": int(os.environ.get("POSTGRES_PORT", 5432)),
        "NAME": os.environ.get("POSTGRES_DB", None),
        "USER": os.environ.get("POSTGRES_USER", None),
        "PASSWORD": os.environ.get("POSTGRES_PASS", None),
    }
}

MIDDLEWARE = (  # noqa
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "allauth.account.middleware.AccountMiddleware",
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

CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = getattr(
    settings, "CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT", False
)

DATA_SORTING_FIELDS = ["+title"]

CUSTOM_NAME = "Curator"
ALLAUTH_ACCOUNT_REQUESTS_FOR_NEW_USERS = True
ACCOUNT_ADAPTER = "core_main_app.utils.allauth.cdcs_adapter.CDCSAccountAdapter"
SOCIALACCOUNT_AUTO_SIGNUP = False
ACCOUNT_SIGNUP_FORM_CLASS = "core_main_app.utils.allauth.forms.CoreSignupForm"
ENABLE_SAML2_SSO_AUTH = False
ENABLE_ALLAUTH = False
VERIFY_DATA_ACCESS = False

USE_TZ = True
CHECKSUM_ALGORITHM = "MD5"
MONGODB_INDEXING = False
MONGODB_ASYNC_SAVE = False
DJANGO_SIMPLE_HISTORY_MODELS = []
BOOTSTRAP_VERSION = "5.1.3"

ID_PROVIDER_SYSTEM_NAME = "mock_provider"
ENABLE_JSON_SCHEMA_SUPPORT = True
TEXT_EDITOR_LIBRARY = None

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
WEBSITE_CONTACTS = [("John", "john@example.com"), ("Mary", "mary@example.com")]
EMAIL_SUBJECT_PREFIX = "[Test]"
