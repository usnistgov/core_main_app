""" Fixtures file for template version manager
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


class TemplateVersionManagerAccessControlFixtures(FixtureInterface):
    """Template Version Manager fixtures"""

    user1_template = None
    user2_template = None
    global_template = None
    user1_tvm = None
    user2_tvm = None
    global_tvm = None
    template_vm_collection = None

    def insert_data(self):
        """Insert a set of Templates and Template Version Managers.

        Returns:

        """
        # Make a connexion with a mock database
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        self.user1_template = Template(
            filename="template1.xsd", content=xsd, hash="hash1", user="1"
        ).save()
        self.user2_template = Template(
            filename="template2.xsd", content=xsd, hash="hash2", user="2"
        ).save()
        self.global_template = Template(
            filename="global_template.xsd", content=xsd, hash="global hash", user=None
        ).save()

        self.user1_tvm = TemplateVersionManager(
            title="template 1",
            user="1",
            versions=[
                str(self.user1_template.id),
            ],
            current=str(self.user1_template.id),
            is_disabled=False,
            disabled_versions=[],
        ).save()

        self.user2_tvm = TemplateVersionManager(
            title="template 2",
            user="2",
            versions=[str(self.user2_template.id)],
            current=str(self.user2_template.id),
            is_disabled=False,
            disabled_versions=[],
        ).save()

        self.global_tvm = TemplateVersionManager(
            title="global template",
            user=None,
            versions=[str(self.global_template.id)],
            current=str(self.global_template.id),
            is_disabled=False,
            disabled_versions=[],
        ).save()

        self.template_vm_collection = [self.user1_tvm, self.user2_tvm, self.global_tvm]
