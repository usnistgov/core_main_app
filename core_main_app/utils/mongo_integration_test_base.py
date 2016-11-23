""" Integration test class base
"""
from mongoengine import connect
from unittest.case import TestCase
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template

MOCK_DATABASE_NAME = 'db_mock'
MOCK_DATABASE_URI = 'mongomock://localhost'


class IntegrationTest(TestCase):

    db = None

    """
        Common methods
    """
    def setUp(self):
        # open an connection to a mock database
        self.db = connect(MOCK_DATABASE_NAME, host='mongomock://localhost')

    def tearDown(self):
        self.cleanDatabase()

    def cleanDatabase(self):
        # clear the mock database for the next test
        if self.db is not None:
            self.db.drop_database(MOCK_DATABASE_NAME)

    """
        Data's methods
    """
    def insert_two_data(self):
        template = IntegrationTest.insert_template()  # Must exist in mongo DB before be usable
        self.data_1 = Data(template, '1', None, 'title', '<tag>value 1</tag>').save()
        self.data_2 = Data(template, '2', None, 'title2', '<tag>value 2</tag>').save()

    """
        Template's methods
    """
    @staticmethod
    def insert_template():
        template = Template()
        xsd = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">' \
              '<xs:element name="tag"></xs:element></xs:schema>'
        template.content = xsd
        template.hash = ""
        template.filename = "filename"
        return template.save()
