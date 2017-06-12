""" Fixtures files for Data
"""
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template


class DataFixtures(FixtureInterface):
    """ Data fixtures
    """
    data_1 = None
    data_2 = None
    template = None
    data_collection = None

    def insert_data(self):
        """ Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_data_collection()

    def generate_data_collection(self):
        """ Generate a Data collection.

        Returns:

        """
        self.data_1 = Data(self.template, '1', None, 'title', '<tag>value 1</tag>').save()
        self.data_2 = Data(self.template, '2', None, 'title2', '<tag>value 2</tag>').save()
        self.data_collection = [self.data_1, self.data_2]

    def generate_template(self):
        """ Generate an unique Template.

        Returns:

        """
        template = Template()
        xsd = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">' \
              '<xs:element name="tag"></xs:element></xs:schema>'
        template.content = xsd
        template.hash = ""
        template.filename = "filename"
        self.template = template.save()
