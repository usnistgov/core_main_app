""" Unit tests for migrations utilities
"""
from django.db import OperationalError
from unittest.mock import patch

from django.test import TestCase

from core_main_app.utils.migrations import ensure_migration_applied
from tests.mocks import MockQuerySet


class TestEnsureMigrationApplied(TestCase):
    """Unit tests for ensure_migration_applied function"""

    @staticmethod
    def patch_migration_object(expected_count):
        mock_migration_qs = MockQuerySet()
        mock_migration_qs.item_list = [None] * expected_count

        return mock_migration_qs

    @patch(
        "django.db.migrations.recorder.MigrationRecorder.Migration.objects.filter"
    )
    def test_migration_applied_exits_succesfully(self, mock_migration):
        mock_migration.return_value = self.patch_migration_object(1)

        self.assertIsNone(
            ensure_migration_applied("mock_app", "mock_migration")
        )

    @patch(
        "django.db.migrations.recorder.MigrationRecorder.Migration.objects.filter"
    )
    def test_migration_not_applied_raises_runtime_error(self, mock_migration):
        mock_migration.return_value = self.patch_migration_object(0)

        with self.assertRaises(RuntimeError):
            ensure_migration_applied("mock_app", "mock_migration")

    @patch(
        "django.db.migrations.recorder.MigrationRecorder.Migration.objects.filter"
    )
    def test_operational_error_is_discarded(self, mock_migration):
        mock_migration.side_effect = OperationalError(
            "mock_migration_operational_error"
        )

        self.assertIsNone(
            ensure_migration_applied("mock_app", "mock_migration")
        )
