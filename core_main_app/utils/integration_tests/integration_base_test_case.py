""" Integration Tests Base
"""
from django.test import TestCase

from core_main_app.commons.exceptions import CoreError


# FIXME: rename, not Mongo
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
