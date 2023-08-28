""" Fixtures file for Templates
"""
from django.core.files.uploadedfile import SimpleUploadedFile

from core_main_app.components.template.models import Template
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)


class AccessControlTemplateFixture(FixtureInterface):
    """Access Control Data fixture"""

    user1_template = None
    user2_template = None
    global_template = None
    template_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template_collection()

    def generate_template_collection(self):
        """Generate a Template Collections.

        Returns:

        """
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        self.user1_template = Template(
            content=xsd,
            _hash="user1_template_hash",
            filename="user1_template.xsd",
            file=SimpleUploadedFile("user1_template.xsd", xsd.encode("utf-8")),
            user="1",
            _cls="Template",
        )
        self.user1_template.save()
        self.user2_template = Template(
            content=xsd,
            _hash="user2_template_hash",
            filename="user2_template.xsd",
            file=SimpleUploadedFile("user2_template.xsd", xsd.encode("utf-8")),
            user="2",
            _cls="Template",
        )
        self.user2_template.save()
        self.global_template = Template(
            content=xsd,
            _hash="global_template_hash",
            filename="global_template.xsd",
            file=SimpleUploadedFile(
                "global_template.xsd", xsd.encode("utf-8")
            ),
            user=None,
            _cls="Template",
        )
        self.global_template.save()
        self.template_collection = [
            self.user1_template,
            self.user2_template,
            self.global_template,
        ]
