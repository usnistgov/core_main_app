""" Integration Tests with transaction
"""
from django.core.management import execute_from_command_line
from django.test.testcases import TransactionTestCase

import core_main_app.permissions.rights as rights
from core_main_app.components.group import api as group_api
from tests.test_settings import database as settings_database


class MongoIntegrationTransactionTestCase(TransactionTestCase):
    """Represent the Integration base transaction test case
    The integration tests must inherit of this class
    """

    """
        Fields
    """
    database = settings_database  # database to use
    fixture = None  # data fixture from component's tests

    """
        Methods
    """

    def setUp(self):
        """Insert needed data.

        Returns:

        """
        self.clear_database()
        group_api.get_or_create(name=rights.anonymous_group)
        group_api.get_or_create(name=rights.default_group)

        if self.fixture is not None:
            self.fixture.insert_data()

    def clear_database(self):
        execute_from_command_line(["", "flush", "--no-input"])
        self.database.clean_database()
