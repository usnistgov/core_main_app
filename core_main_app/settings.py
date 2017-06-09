from django.conf import settings

if not settings.configured:
    settings.configure()

SECRET_KEY = getattr(settings, 'SECRET_KEY', '<secret_key>')

SERVER_URI = getattr(settings, 'SERVER_URI', "http://127.0.0.1:8000")

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])

# Website configuration
WEBSITE_COMPACT_TITLE = getattr(settings, 'WEBSITE_COMPACT_TITLE', "Project")

# Choose from:  black, black-light, blue, blue-light, green, green-light, purple, purple-light, red, red-light, yellow,
#               yellow-light
WEBSITE_ADMIN_COLOR = getattr(settings, 'WEBSITE_ADMIN_COLOR', "yellow")

# XML
XERCES_VALIDATION = getattr(settings, 'XERCES_VALIDATION', False)

# GridFS
GRIDFS_DATA_COLLECTION = getattr(settings, 'GRIDFS_DATA_COLLECTION', 'fs_data')

# Celery configuration
USE_BACKGROUND_TASK = getattr(settings, 'USE_BACKGROUND_TASK', False)
BROKER_URL = getattr(settings, 'BROKER_URL', 'redis://localhost:6379/0')

broker_transport_default = {
    "visibility_timeout": 3600,
    'fanout_prefix': True,
    'fanout_patterns': True
}
BROKER_TRANSPORT_OPTIONS = getattr(settings, 'BROKER_TRANSPORT_OPTIONS', broker_transport_default)
CELERY_RESULT_BACKEND = getattr(settings, 'CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# SMTP Configuration
USE_EMAIL = getattr(settings, 'USE_EMAIL', False)
SERVER_EMAIL = getattr(settings, 'SERVER_EMAIL', 'noreply@curator.org')
ADMINS = getattr(settings, 'ADMINS', [('admin', 'admin@curator.org')])
MANAGERS = getattr(settings, 'MANAGERS', [('manager', 'moderator@curator.org')])
EMAIL_SUBJECT_PREFIX = getattr(settings, 'EMAIL_SUBJECT_PREFIX', "[CURATOR] ")


# Replace by your own values
MONGO_USER = getattr(settings, 'MONGO_USER', "mgi_user")
MONGO_PASSWORD = getattr(settings, 'MONGO_PASSWORD', "mgi_password")
DB_NAME = getattr(settings, 'DB_NAME', "mgi")

mongodb_uri_default = "mongodb://" + MONGO_USER + ":" + MONGO_PASSWORD + "@localhost/" + DB_NAME
MONGODB_URI = getattr(settings, 'MONGODB_URI', mongodb_uri_default)

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])

DATA_AUTO_PUBLISH = getattr(settings, 'DATA_AUTO_PUBLISH', False)

USE_TZ = getattr(settings, 'USE_TZ', True)

SEARCHABLE_DATA_OCCURRENCES_LIMIT = getattr(settings, 'SEARCHABLE_DATA_OCCURRENCES_LIMIT', None)

BLOB_HOST = getattr(settings, 'BLOB_HOST', 'GRIDFS')
BLOB_HOST_URI = getattr(settings, 'BLOB_HOST_URI', MONGODB_URI)
BLOB_HOST_USER = getattr(settings, 'BLOB_HOST_USER', None)
BLOB_HOST_PASSWORD = getattr(settings, 'BLOB_HOST_PASSWORD', None)

PASSWORD_MIN_LENGTH = getattr(settings, 'PASSWORD_MIN_LENGTH', 0)
PASSWORD_MIN_LOWERCASE_LETTERS = getattr(settings, 'PASSWORD_MIN_LOWERCASE_LETTERS', 0)
PASSWORD_MIN_UPPERCASE_LETTERS = getattr(settings, 'PASSWORD_MIN_UPPERCASE_LETTERS', 0)
