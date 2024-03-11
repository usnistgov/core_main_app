""" Migration utilities
"""
import logging

from django.db import OperationalError
from django.db.migrations.recorder import MigrationRecorder

logger = logging.getLogger(__name__)


def ensure_migration_applied(app_name, migration_name):
    """Check that a given migration has been applied. Raises RuntimeError if
    it is not the case.

    Inspired by https://stackoverflow.com/a/50100972/1723284.
    """
    try:
        migrations = MigrationRecorder.Migration.objects.filter(
            app=app_name, name=migration_name
        )

        if migrations.count() != 1:
            error_message = f"Migration ({app_name}, {migration_name}) needs to be applied!"

            logger.error(error_message)
            raise RuntimeError(error_message)
    except OperationalError as exc:
        logger.warning(
            "An error occured while checking the status of the "
            f"({app_name}, {migration_name}) migration: {exc}"
        )
