""" Integration Tests Base
"""
from django.test import TestCase

from core_main_app.commons.exceptions import CoreError
from core_main_app.settings import MONGODB_INDEXING

MOCK_DATABASE_NAME = "db_mock"
MOCK_DATABASE_HOST = "mongomock://localhost"


class MongoIntegrationBaseTestCase(TestCase):
    """Represent the Integration base test case
    The integration tests must inherit of this class
    """

    """
        Fields
    """
    database = None  # database to use
    fixture = None  # data fixture from component's tests

    """
        Methods
    """

    def setUp(self):
        """Insert needed data.

        Returns:

        """
        if self.fixture is None:
            raise CoreError("Fixtures must be initialized")

        self.fixture.insert_data()

    @classmethod
    def setUpClass(cls):
        """Open a connection to the database.

        Returns:

        """
        if MONGODB_INDEXING:
            from core_main_app.utils.databases.mongo.mongoengine_database import (
                Database,
            )

            # open a connection to a mock database
            cls.database = Database(MOCK_DATABASE_HOST, MOCK_DATABASE_NAME)
            cls.database.connect()

    @classmethod
    def tearDownClass(cls):
        """Disconnect the database.
        Returns:

        """
        if MONGODB_INDEXING:
            cls.database.disconnect()

    def tearDown(self):
        """Clean the database.

        Returns:

        """
        if MONGODB_INDEXING:
            self.database.clean_database()
