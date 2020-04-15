""" Settings for core_main_app. These settings are overwritten at project level.
"""
import os
from os.path import join

from django.conf import settings

if not settings.configured:
    settings.configure()

CUSTOM_NAME = getattr(settings, 'CUSTOM_NAME', 'Local')
""" :py:class:`str`: Name of the local instance
"""

SECRET_KEY = getattr(settings, 'SECRET_KEY', '<secret_key>')
""" :py:class:`str`: Django application secret key.
"""

SERVER_URI = getattr(settings, 'SERVER_URI', "http://127.0.0.1:8000")
""" :py:class:`str`: Server URI for import reference.
"""

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])
""" :py:class:`list`: List of apps installed.
"""

# Website configuration
WEBSITE_COMPACT_TITLE = getattr(settings, 'WEBSITE_COMPACT_TITLE', "Project")
""" :py:class:`str`: Website title.
"""

# Choose from:  black, black-light, blue, blue-light, green, green-light, purple, purple-light, red, red-light, yellow,
#               yellow-light
WEBSITE_ADMIN_COLOR = getattr(settings, 'WEBSITE_ADMIN_COLOR', "yellow")
""" :py:class:`str`: color of the admin dashboard.
"""

# XML
XERCES_VALIDATION = getattr(settings, 'XERCES_VALIDATION', False)
""" :py:class:`bool`: Enables Xerces validation (requires additional packages).
"""

# GridFS
GRIDFS_DATA_COLLECTION = getattr(settings, 'GRIDFS_DATA_COLLECTION', 'fs_data')
""" :py:class:`str`: Collection name for file storage in MongoDB.
"""

# Celery configuration
USE_BACKGROUND_TASK = getattr(settings, 'USE_BACKGROUND_TASK', False)
""" :py:class:`bool`: Define use of celery for background tasks.
"""

BROKER_URL = getattr(settings, 'BROKER_URL', 'redis://localhost:6379/0')
""" :py:class:`str`: Celery broker address.
"""

broker_transport_default = {
    "visibility_timeout": 3600,
    'fanout_prefix': True,
    'fanout_patterns': True
}
BROKER_TRANSPORT_OPTIONS = getattr(settings, 'BROKER_TRANSPORT_OPTIONS', broker_transport_default)
""" :py:class:`dict`: Celery broker options.
"""

CELERY_RESULT_BACKEND = getattr(settings, 'CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
""" :py:class:`str`: Celery backend for results.
"""

# SMTP Configuration
USE_EMAIL = getattr(settings, 'USE_EMAIL', False)
""" :py:class:`bool`: Activate email sending on the platform.
"""

SERVER_EMAIL = getattr(settings, 'SERVER_EMAIL', 'noreply@example.com')
""" :py:class:`str`: Email address sending the message.
"""

ADMINS = getattr(settings, 'ADMINS', [('admin', 'admin@example.com')])
""" :py:class:`list`: Email addresses of admins.
"""

MANAGERS = getattr(settings, 'MANAGERS', [('manager', 'moderator@example.com')])
""" :py:class:`list`: Email addresses of moderators (managers). 
"""

EMAIL_SUBJECT_PREFIX = getattr(settings, 'EMAIL_SUBJECT_PREFIX', "[CURATOR] ")
""" :py:class:`str`: Prefix for easy classification of emails.
"""

MONGO_USER = getattr(settings, 'MONGO_USER', "mgi_user")
""" :py:class:`str`: MongoDB user.
"""

MONGO_PASSWORD = getattr(settings, 'MONGO_PASSWORD', "mgi_password")
""" :py:class:`str`: MongoDB password.
"""

DB_NAME = getattr(settings, 'DB_NAME', "mgi")
""" :py:class:`str`: MongoDB password.
"""

mongodb_uri_default = "mongodb://" + MONGO_USER + ":" + MONGO_PASSWORD + "@localhost/" + DB_NAME
MONGODB_URI = getattr(settings, 'MONGODB_URI', mongodb_uri_default)
""" :py:class:`str`: MongoDB connection URI. Automatically generated from other parameters.
"""

USE_TZ = getattr(settings, 'USE_TZ', True)
""" :py:class:`bool`: Activate use of timezones.
"""

SEARCHABLE_DATA_OCCURRENCES_LIMIT = getattr(settings, 'SEARCHABLE_DATA_OCCURRENCES_LIMIT', None)
""" :py:class:`int` | :py:attr:`None`: Limit for number of occurent to be returned by a search.
"""

BLOB_HOST = getattr(settings, 'BLOB_HOST', 'GRIDFS')
""" :py:class:`str`: Type of file storage.
"""

BLOB_HOST_URI = getattr(settings, 'BLOB_HOST_URI', MONGODB_URI)
""" :py:class:`str`: File storage system URI.
"""

BLOB_HOST_USER = getattr(settings, 'BLOB_HOST_USER', None)
""" :py:class:`str`: User for file storage.
"""

BLOB_HOST_PASSWORD = getattr(settings, 'BLOB_HOST_PASSWORD', None)
""" :py:class:`str`: Password for file storage.
"""

# Password settings for django.contrib.auth validators
PASSWORD_MIN_LENGTH = getattr(settings, 'PASSWORD_MIN_LENGTH', 0)
""" :py:class:`int`: Required minimum length of a password.
"""

PASSWORD_MIN_LOWERCASE_LETTERS = getattr(settings, 'PASSWORD_MIN_LOWERCASE_LETTERS', 0)
""" :py:class:`int`: Required number of lowercase chars in a password.
"""

PASSWORD_MIN_UPPERCASE_LETTERS = getattr(settings, 'PASSWORD_MIN_UPPERCASE_LETTERS', 0)
""" :py:class:`int`: Required number of uppercase chars in a password.
"""

PASSWORD_MIN_LETTERS = getattr(settings, 'PASSWORD_MIN_LETTERS', 0)
""" :py:class:`int`: Specifies the minimum amount of required letters in a password.
"""

PASSWORD_MIN_NUMBERS = getattr(settings, 'PASSWORD_MIN_NUMBERS', 0)
""" :py:class:`int`: Specifies the minimum amount of required numbers in a password.
"""

PASSWORD_MIN_SYMBOLS = getattr(settings, 'PASSWORD_MIN_SYMBOLS', 0)
""" :py:class:`int`: Specifies the minimum amount of required symbols in a password.
"""

PASSWORD_MAX_OCCURRENCE = getattr(settings, 'PASSWORD_MAX_OCCURRENCE', None)
""" :py:class:`int`: Specifies the maximum amount of consecutive characters allowed in passwords.
"""

# Lock
LOCK_OBJECT_TTL = getattr(settings, 'LOCK_OBJECT_TTL', 600)  # 10 min
""" :py:class:`int`: Lock duration on files.
"""

# Results per page for paginator
RESULTS_PER_PAGE = getattr(settings, 'RESULTS_PER_PAGE', 10)
""" :py:class:`int`: Results per page.
"""

CAN_SET_PUBLIC_DATA_TO_PRIVATE = getattr(settings, 'CAN_SET_PUBLIC_DATA_TO_PRIVATE', True)
""" :py:class:`bool`: Can set public data to private.
"""

DEFAULT_DATA_RENDERING_XSLT = getattr(settings, 'DEFAULT_DATA_RENDERING_XSLT',
                                      join('core_main_app', 'common', 'xsl', 'xml2html.xsl'))
""" :py:class:`str`: Path to default XSLT to render data.
"""

# Can anonymous access public document
CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = getattr(settings, 'CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT', False)
""" :py:class:`bool`: Can anonymous user access public document.
"""

DISPLAY_NIST_HEADERS = getattr(settings, 'DISPLAY_NIST_HEADERS', False)
""" :py:class:`bool`: HTML pages show the NIST headers/footers.
"""

# Locale folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
""" :py:class:`str`: Project installation directory.
"""

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'core_main_app/locale'),
)
""" :py:class:`list`: Path for translation messages.
"""

CAN_SET_WORKSPACE_PUBLIC = getattr(settings, 'CAN_SET_WORKSPACE_PUBLIC', True)
""" :py:class:`bool`: Can set workspace public.
"""

SSL_CERTIFICATES_DIR = getattr(settings, 'SSL_CERTIFICATES_DIR', True)
""" :py:class:`str`: SSL certificates directory location.
"""

XSD_URI_RESOLVER = getattr(settings, 'XSD_URI_RESOLVER', None)
""" :py:class:`str`: XSD URI Resolver for lxml validation. Choose from:  None, 'REQUESTS_RESOLVER'.
"""

VERIFY_DATA_ACCESS = getattr(settings, 'VERIFY_DATA_ACCESS', False)
""" :py:class:`bool`: Verify that data returned by a query can be accessed.
"""

DATA_SORTING_FIELDS = getattr(settings, 'DATA_SORTING_FIELDS', [])
""" ::py:class:`str` Set the default sort fields for the data query. all the field must be prefixed by "+" or "-" (asc or desc sort)
    the sort can be multi field and each field must be delimited by "," (ex. ["-title","+name","+date"]) 
"""
