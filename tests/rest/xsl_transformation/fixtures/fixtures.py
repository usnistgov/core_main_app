""" Fixtures files for XslTransformation
"""
from django.core.files.uploadedfile import SimpleUploadedFile

from core_main_app.components.xsl_transformation.models import XslTransformation
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface


class XslTransformationFixtures(FixtureInterface):
    """Xsl Transformation fixtures"""

    data_1 = None
    data_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a Data collection.

        Returns:

        """
        content = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">'
            '<xsl:template match="/"></xsl:template></xsl:stylesheet>'
        )
        self.data_1 = XslTransformation(
            name="name_1",
            filename="filename_1.xsd",
            file=SimpleUploadedFile(
                "xsl_transformation.xsl", content=content.encode("utf-8")
            ),
        )
        self.data_1.save()
        self.data_collection = [self.data_1]
