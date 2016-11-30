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
    def setUp(self):
        """ Open a connection to the database and insert data needed

        Returns:

        """
        # open an connection to a mock database
        self.database = Database(MOCK_DATABASE_HOST, MOCK_DATABASE_NAME)
        self.database.connect()

        if self.fixture is None:
            raise CoreError("Fixtures must be initialized")

        self.fixture.insert_data()

    # FIXME: /!\ collections are kept between tests in a same class
    def tearDown(self):
        """ Clean the database

        Returns:

        """
        self.database.clean_database()
        self.database = None
