from core_main_app.utils.databases.mongoengine_database import Database

SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',

    # Extra apps
    "password_policies",

    # Local apps
    "core_main_app",
    "tests",
]

# IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}


PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
)

MOCK_DATABASE_NAME = 'db_mock'
MOCK_DATABASE_HOST = 'mongomock://localhost'

database = Database(MOCK_DATABASE_HOST, MOCK_DATABASE_NAME)
database.connect()
