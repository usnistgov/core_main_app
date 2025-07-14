""" Fixtures file for Templates """

from django.core.files.uploadedfile import SimpleUploadedFile

from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)


class AccessControlTemplateFixture(FixtureInterface):
    """Access Control Data fixture"""

    user1_template = None
    user2_template = None
    global_template = None
    template_collection = None
    user1_version_manager = None
    user2_version_manager = None
    global_version_manager = None

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

        # Create version managers
        self.user1_version_manager = TemplateVersionManager(
            user="1", title="Template User 1"
        )
        self.user1_version_manager.save()
        self.user2_version_manager = TemplateVersionManager(
            user="2", title="Template User 2"
        )
        self.user2_version_manager.save()
        self.global_version_manager = TemplateVersionManager(
            user=None, title="Template Global"
        )
        self.global_version_manager.save()

        # Create templates with version managers
        self.user1_template = Template(
            content=xsd,
            _hash="user1_template_hash",
            filename="user1_template.xsd",
            file=SimpleUploadedFile("user1_template.xsd", xsd.encode("utf-8")),
            user="1",
            _cls="Template",
            version_manager=self.user1_version_manager,
        )
        self.user1_template.save()

        self.user2_template = Template(
            content=xsd,
            _hash="user2_template_hash",
            filename="user2_template.xsd",
            file=SimpleUploadedFile("user2_template.xsd", xsd.encode("utf-8")),
            user="2",
            _cls="Template",
            version_manager=self.user2_version_manager,
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
            version_manager=self.global_version_manager,
        )
        self.global_template.save()

        self.template_collection = [
            self.user1_template,
            self.user2_template,
            self.global_template,
        ]
