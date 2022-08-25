""" Integration Tests with transaction
"""
from django.core.management import execute_from_command_line
from django.test.testcases import TransactionTestCase

from core_main_app.components.group import api as group_api
from core_main_app.permissions import rights
from core_main_app.settings import MONGODB_INDEXING


class MongoIntegrationTransactionTestCase(TransactionTestCase):
    """Represent the Integration base transaction test case
    The integration tests must inherit of this class
    """

    """
        Fields
    """
    fixture = None  # data fixture from component's tests
    if MONGODB_INDEXING:
        from tests.test_settings_mongo import database as settings_database

        database = settings_database

    """
        Methods
    """

    def setUp(self):
        """Insert needed data.

        Returns:

        """
        self.clear_database()
        group_api.get_or_create(name=rights.ANONYMOUS_GROUP)
        group_api.get_or_create(name=rights.DEFAULT_GROUP)

        if self.fixture is not None:
            self.fixture.insert_data()

    def clear_database(self):
        """clear_database

        Returns:

        """
        execute_from_command_line(["", "flush", "--no-input"])
        if MONGODB_INDEXING:
            self.database.clean_database()
