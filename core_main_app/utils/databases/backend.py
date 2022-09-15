"""Utils for database backend
"""
from django.conf import settings

POSTGRESQL_BACKEND = "django.db.backends.postgresql_psycopg2"
SQLITE3_BACKEND = "django.db.backends.sqlite3"


def get_default_database_engine():
    """Get default engine

    Returns:

    """
    return settings.DATABASES["default"]["ENGINE"]


def uses_postgresql_backend():
    """Returns True if PostgreSQL backend

    Returns:

    """
    return get_default_database_engine() == POSTGRESQL_BACKEND


def uses_sqlite3_backend():
    """Returns True if SQLite3 backend

    Returns:

    """
    return get_default_database_engine() == SQLITE3_BACKEND
