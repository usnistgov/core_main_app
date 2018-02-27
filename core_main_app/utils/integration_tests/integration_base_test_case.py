""" Integration Tests Base
"""
from django.test.testcases import SimpleTestCase

from core_main_app.commons.exceptions import CoreError
from tests.test_settings import database as settings_database


class MongoIntegrationBaseTestCase(SimpleTestCase):
    """ Represent the Integration base test case
        The integration tests must inherit of this class
    """

    """
        Fields
    """
    database = settings_database     # database to use
    fixture = None      # data fixture from component's tests

    """
        Methods
    """

    def setUp(self):
        """ Insert needed data.

        Returns:

        """
        if self.fixture is None:
            raise CoreError("Fixtures must be initialized")

        self.fixture.insert_data()

    def tearDown(self):
        """ Clean the database.

        Returns:

        """
        self.database.clean_database()
