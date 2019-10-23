from core_main_app.utils.databases.mongoengine_database import Database

SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',

    # Extra apps
    "defender",

    # Local apps
    "core_main_app",
    "tests",
]

# SERVER URI
SERVER_URI = "http://my.curator.com"

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

DATA_SORTING_FIELDS = ['+title']

# Password settings for django.contrib.auth validators
# Specifies the minimum length for passwords.
PASSWORD_MIN_LENGTH = 12
# Specifies the minimum amount of required letters in a password.
PASSWORD_MIN_LETTERS = 1
# Specifies the minimum amount of required uppercase letters in a password.
PASSWORD_MIN_UPPERCASE_LETTERS = 1
# Specifies the minimum amount of required lowercase letters in a password.
PASSWORD_MIN_LOWERCASE_LETTERS = 1
# Specifies the minimum amount of required numbers in a password.
PASSWORD_MIN_NUMBERS = 1
# Specifies the minimum amount of required symbols in a password.
PASSWORD_MIN_SYMBOLS = 1
# Specifies the maximum amount of consecutive characters allowed in passwords.
PASSWORD_MAX_OCCURRENCE = 5

database = Database(MOCK_DATABASE_HOST, MOCK_DATABASE_NAME)
database.connect()
