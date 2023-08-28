""" Fixtures file for template version manager
"""
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)


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
        self.template_vm_1 = TemplateVersionManager(
            title="template 1",
            user=None,
            is_disabled=False,
        )
        self.template_vm_1.save_version_manager()
        self.template_1_1 = Template(
            filename="template1_1.xsd",
            content="content1_1",
            _hash="hash1_1",
            version_manager=self.template_vm_1,
        )
        self.template_1_1.save()
        self.template_1_2 = Template(
            filename="template1_2.xsd",
            content="content1_2",
            _hash="hash1_2",
            is_disabled=True,
            version_manager=self.template_vm_1,
        )
        self.template_1_2.save()
        self.template_1_3 = Template(
            filename="template1_3.xsd",
            content="content1_3",
            _hash="hash1_3",
            is_current=True,
            version_manager=self.template_vm_1,
        )
        self.template_1_3.save()

        self.template_vm_2 = TemplateVersionManager(
            title="template 2",
            user="1",
            is_disabled=False,
        )
        self.template_vm_2.save_version_manager()
        self.template_2_1 = Template(
            filename="template2_1.xsd",
            content="content2_1",
            _hash="hash2_1",
            is_current=True,
            version_manager=self.template_vm_2,
        )
        self.template_2_1.save()

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

        self.user1_tvm = TemplateVersionManager(
            title="template 1",
            user="1",
            is_disabled=False,
        )
        self.user1_tvm.save_version_manager()

        self.user2_tvm = TemplateVersionManager(
            title="template 2",
            user="2",
            is_disabled=False,
        )
        self.user2_tvm.save_version_manager()

        self.global_tvm = TemplateVersionManager(
            title="global template",
            user=None,
            is_disabled=False,
        )
        self.global_tvm.save_version_manager()

        self.user1_template = Template(
            filename="template1.xsd",
            content=xsd,
            _hash="hash1",
            user="1",
            is_current=True,
            version_manager=self.user1_tvm,
        )
        self.user1_template.save()
        self.user2_template = Template(
            filename="template2.xsd",
            content=xsd,
            _hash="hash2",
            user="2",
            is_current=True,
            version_manager=self.user2_tvm,
        )
        self.user2_template.save()
        self.global_template = Template(
            filename="global_template.xsd",
            content=xsd,
            _hash="global hash",
            user=None,
            is_current=True,
            version_manager=self.global_tvm,
        )
        self.global_template.save()

        self.template_vm_collection = [
            self.user1_tvm,
            self.user2_tvm,
            self.global_tvm,
        ]


class TemplateVersionManagerOrderingFixtures(FixtureInterface):
    """Template Version Manager Ordering fixtures"""

    user1_template = None
    global_template = None
    tvm1 = None
    tvm2 = None
    global_tvm1 = None
    global_tvm2 = None
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

        self.tvm1 = TemplateVersionManager(
            title="template 1",
            user="1",
            is_disabled=False,
        )
        self.tvm1.save_version_manager()

        self.tvm2 = TemplateVersionManager(
            title="template 2",
            user="1",
            is_disabled=False,
        )
        self.tvm2.save_version_manager()

        self.global_tvm1 = TemplateVersionManager(
            title="global template1",
            user=None,
            is_disabled=False,
        )
        self.global_tvm1.save_version_manager()

        self.global_tvm2 = TemplateVersionManager(
            title="global template2",
            user=None,
            is_disabled=False,
        )
        self.global_tvm2.save_version_manager()

        self.user1_template = Template(
            filename="template1.xsd",
            content=xsd,
            _hash="hash1",
            user="1",
            is_current=True,
            version_manager=self.tvm1,
        )
        self.user1_template.save()

        self.global_template = Template(
            filename="global_template.xsd",
            content=xsd,
            _hash="global hash",
            user=None,
            is_current=True,
            version_manager=self.global_tvm1,
        )
        self.global_template.save()

        self.template_vm_collection = [
            self.tvm1,
            self.tvm2,
            self.global_tvm1,
            self.global_tvm2,
        ]
