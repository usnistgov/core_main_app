""" Integration Tests Base
"""

from core_main_app.commons.exceptions import CoreError
from core_main_app.utils.databases.mongoengine_database import Database
from unittest.case import TestCase

MOCK_DATABASE_NAME = 'db_mock'
MOCK_DATABASE_HOST = 'mongomock://localhost'


class MongoIntegrationBaseTestCase(TestCase):
    """ Represents the Integration base test case
        The integration tests must inherit of this class
    """

    """
        Fields
    """
    database = None     # database to use
    fixture = None      # data fixture from component's tests

    """
        Methods
    """

    @classmethod
    def setUpClass(cls):
        """ Opens a connection to the database.

        Returns:

        """
        # open an connection to a mock database
        cls.database = Database(MOCK_DATABASE_HOST, MOCK_DATABASE_NAME)
        cls.database.connect()

    @classmethod
    def tearDownClass(cls):
        """ Disconnects the database.
        Returns:

        """
        cls.database.disconnect()

    def setUp(self):
        """ Inserts needed data.

        Returns:

        """
        if self.fixture is None:
            raise CoreError("Fixtures must be initialized")

        self.fixture.insert_data()

    def tearDown(self):
        """ Cleans the database.

        Returns:

        """
        self.database.clean_database()
