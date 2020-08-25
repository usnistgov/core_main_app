""" Fixtures files for template version manager
"""
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface


class TemplateVersionManagerFixtures(FixtureInterface):
    """Template Version Manager fixtures"""

    template_1_1 = None
    template_1_2 = None
    template_1_3 = None
    template_2_1 = None
    template_vm_1 = None
    template_vm_2 = None
    template_vm_collection = None

    def insert_data(self):
        """Insert a set of Templates and Template Version Managers.

        Returns:

        """
        # Make a connexion with a mock database
        self.template_1_1 = Template(
            filename="template1_1.xsd", content="content1_1", hash="hash1_1"
        ).save()
        self.template_1_2 = Template(
            filename="template1_2.xsd", content="content1_2", hash="hash1_2"
        ).save()
        self.template_1_3 = Template(
            filename="template1_3.xsd", content="content1_3", hash="hash1_3"
        ).save()
        self.template_2_1 = Template(
            filename="template2_1.xsd", content="content2_1", hash="hash2_1"
        ).save()

        self.template_vm_1 = TemplateVersionManager(
            title="template 1",
            user=None,
            versions=[
                str(self.template_1_1.id),
                str(self.template_1_2.id),
                str(self.template_1_3.id),
            ],
            current=str(self.template_1_3.id),
            is_disabled=False,
            disabled_versions=[str(self.template_1_2.id)],
        ).save()

        self.template_vm_2 = TemplateVersionManager(
            title="template 2",
            user="1",
            versions=[str(self.template_2_1.id)],
            current=str(self.template_2_1.id),
            is_disabled=False,
            disabled_versions=[],
        ).save()

        self.template_vm_collection = [self.template_vm_1, self.template_vm_2]
