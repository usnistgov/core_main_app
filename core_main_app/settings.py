""" Core main app settings
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

SECRET_KEY = getattr(settings, 'SECRET_KEY', '<secret_key>')
""" str: Django application secret key
"""

SERVER_URI = getattr(settings, 'SERVER_URI', "http://127.0.0.1:8000")
""" str: Server URI for import reference
"""

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])
""" list: List of apps installed
"""

# Website configuration
WEBSITE_COMPACT_TITLE = getattr(settings, 'WEBSITE_COMPACT_TITLE', "Project")
""" str: Website title
"""

# Choose from:  black, black-light, blue, blue-light, green, green-light, purple, purple-light, red, red-light, yellow,
#               yellow-light
WEBSITE_ADMIN_COLOR = getattr(settings, 'WEBSITE_ADMIN_COLOR', "yellow")
""" str: color of the admin dashboard
"""

# XML
XERCES_VALIDATION = getattr(settings, 'XERCES_VALIDATION', False)
""":py:class:`bool`: Enables Xerces validation (requires additional packages).
"""

# GridFS
GRIDFS_DATA_COLLECTION = getattr(settings, 'GRIDFS_DATA_COLLECTION', 'fs_data')
""" str: Collection name for file storage in MongoDB.
"""

# Celery configuration
USE_BACKGROUND_TASK = getattr(settings, 'USE_BACKGROUND_TASK', False)
""" bool: Define use of celery for background tasks
"""

BROKER_URL = getattr(settings, 'BROKER_URL', 'redis://localhost:6379/0')
""" str: Celery broker address
"""

broker_transport_default = {
    "visibility_timeout": 3600,
    'fanout_prefix': True,
    'fanout_patterns': True
}
BROKER_TRANSPORT_OPTIONS = getattr(settings, 'BROKER_TRANSPORT_OPTIONS', broker_transport_default)
""" dict: Celery broker options
"""

CELERY_RESULT_BACKEND = getattr(settings, 'CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
""" str: Celery backend for results
"""

# SMTP Configuration
USE_EMAIL = getattr(settings, 'USE_EMAIL', False)
""" bool: Activate email sending on the platform
"""

SERVER_EMAIL = getattr(settings, 'SERVER_EMAIL', 'noreply@curator.org')
""" str: Email address sending the message.
"""

ADMINS = getattr(settings, 'ADMINS', [('admin', 'admin@curator.org')])
""" list: Email addresses of admins.
"""

MANAGERS = getattr(settings, 'MANAGERS', [('manager', 'moderator@curator.org')])
""" list: Email addresses of moderators (managers). 
"""

EMAIL_SUBJECT_PREFIX = getattr(settings, 'EMAIL_SUBJECT_PREFIX', "[CURATOR] ")
""" str: Prefix for easy classification of emails.
"""

# Replace by your own values
MONGO_USER = getattr(settings, 'MONGO_USER', "mgi_user")
MONGO_PASSWORD = getattr(settings, 'MONGO_PASSWORD', "mgi_password")
DB_NAME = getattr(settings, 'DB_NAME', "mgi")

mongodb_uri_default = "mongodb://" + MONGO_USER + ":" + MONGO_PASSWORD + "@localhost/" + DB_NAME
MONGODB_URI = getattr(settings, 'MONGODB_URI', mongodb_uri_default)

USE_TZ = getattr(settings, 'USE_TZ', True)
""" bool: Activate use of timezones
"""

SEARCHABLE_DATA_OCCURRENCES_LIMIT = getattr(settings, 'SEARCHABLE_DATA_OCCURRENCES_LIMIT', None)
""" :py:class:`int` | :py:attr:`None`: Limit for number of occurent to be returned by a search
"""

BLOB_HOST = getattr(settings, 'BLOB_HOST', 'GRIDFS')
""" str: Type of file storage
"""

BLOB_HOST_URI = getattr(settings, 'BLOB_HOST_URI', MONGODB_URI)
""" str: File storage system URI
"""

BLOB_HOST_USER = getattr(settings, 'BLOB_HOST_USER', None)
""" str: User for file storage
"""

BLOB_HOST_PASSWORD = getattr(settings, 'BLOB_HOST_PASSWORD', None)
""" str: Password for file storage
"""

PASSWORD_MIN_LENGTH = getattr(settings, 'PASSWORD_MIN_LENGTH', 0)
""" int: Required minimum length of a password
"""

PASSWORD_MIN_LOWERCASE_LETTERS = getattr(settings, 'PASSWORD_MIN_LOWERCASE_LETTERS', 0)
""" int: Required number of lowercase chars in a password
"""

PASSWORD_MIN_UPPERCASE_LETTERS = getattr(settings, 'PASSWORD_MIN_UPPERCASE_LETTERS', 0)
""" int: Required number of uppercase chars in a password
"""

# Lock
LOCK_OBJECT_TTL = getattr(settings, 'LOCK_OBJECT_TTL', 600)  # 10 min
""" int: Lock duration on files
"""

# Results per page for paginator
RESULTS_PER_PAGE = getattr(settings, 'RESULTS_PER_PAGE', 10)
""" int: Results per page
"""

CAN_SET_PUBLIC_DATA_TO_PRIVATE = getattr(settings, 'CAN_SET_PUBLIC_DATA_TO_PRIVATE', True)
""" bool: Can set public data to private
"""

