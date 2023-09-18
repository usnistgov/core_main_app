""" Access control fixture for views
"""
from core_main_app.components.blob.models import Blob
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.workspace.models import Workspace
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)
from django.core.files.uploadedfile import SimpleUploadedFile


class AccessControlDataFixture(FixtureInterface):
    """Access Control Data fixture"""

    USER_1_NO_WORKSPACE = 0
    USER_2_NO_WORKSPACE = 1
    USER_1_WORKSPACE_1 = 2
    USER_2_WORKSPACE_2 = 3

    template = None
    workspace_1 = None
    workspace_2 = None
    public_workspace = None
    data_collection = None
    data_1 = None
    data_2 = None
    data_workspace_1 = None
    data_public_workspace = None
    blob_1 = None
    blob_2 = None
    blob_workspace_1 = None
    blob_public_workspace = None
    blob_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_workspaces()
        self.generate_blob_collection()
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a Data collection.

        Returns:

        """

        xml_content = "<root><element>value2</element></root>"
        content = {"root": {"element": "value2"}}

        self.data_1 = Data(
            template=self.template,
            title="Data 1",
            user_id="1",
            xml_content="<root></root>",
        )
        self.data_1.save()
        self.data_2 = Data(
            template=self.template,
            title="Data 2",
            user_id="2",
            xml_content="<root></root>",
        )
        self.data_2.save()
        self.data_public_workspace = Data(
            template=self.template,
            title="Data Public Workspace",
            user_id="1",
            workspace=self.public_workspace,
            xml_content=xml_content,
            dict_content=content,
        )
        self.data_public_workspace.save()
        self.data_workspace_1 = Data(
            template=self.template,
            title="Data Workspace 1",
            user_id="1",
            workspace=self.workspace_1,
            xml_content=xml_content,
            dict_content=content,
        )
        self.data_workspace_1.save()
        self.data_collection = [
            self.data_1,
            self.data_2,
            self.data_public_workspace,
            self.data_workspace_1,
        ]

    def generate_blob_collection(self):
        """Generate a Data collection.

        Returns:

        """
        self.blob_1 = Blob(
            filename="blob1.txt",
            user_id="1",
        )
        self.blob_1.save()
        self.blob_2 = Blob(
            filename="blob2.txt",
            user_id="2",
        )
        self.blob_2.save()
        self.blob_public_workspace = Blob(
            filename="blob3.txt",
            user_id="1",
            workspace=self.public_workspace,
        )
        self.blob_public_workspace.save()
        self.blob_workspace_1 = Blob(
            filename="blob4.txt",
            user_id="1",
            workspace=self.workspace_1,
        )
        self.blob_workspace_1.save()
        self.blob_collection = [
            self.blob_1,
            self.blob_2,
            self.public_workspace,
            self.workspace_1,
        ]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        self.template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="root"></xs:element></xs:schema>'
        )
        self.template.user = "1"
        self.template.content = xsd
        self.template.hash = ""
        self.template.file = SimpleUploadedFile(
            "user1_template.xsd", xsd.encode("utf-8")
        )
        self.template.filename = "filename.xsd"
        self.template.save()

    def generate_workspaces(self):
        """Generate the workspaces.

        Returns:

        """
        self.workspace_1 = Workspace(
            title="Workspace 1", owner="1", read_perm_id="1", write_perm_id="1"
        )
        self.workspace_1.save()
        self.workspace_2 = Workspace(
            title="Workspace 2", owner="2", read_perm_id="2", write_perm_id="2"
        )
        self.workspace_2.save()
        self.public_workspace = Workspace(
            title="Public",
            owner="1",
            read_perm_id="3",
            write_perm_id="3",
            is_public=True,
        )
        self.public_workspace.save()


class JSONDataFixtures(FixtureInterface):
    """Data structure fixtures"""

    data_1 = None
    data_2 = None
    data_3 = None
    data_4 = None

    template = None
    data_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a Data collection.

        Returns:

        """
        content = """
                        {
          "name": "John Doe",
          "age": 30
        }
        """
        self.data_1 = Data(
            template=self.template,
            user_id="1",
            dict_content=None,
            title="title_json",
            content=content,
        )
        self.data_1.save()

        self.data_2 = Data(
            template=self.template,
            user_id="1",
            dict_content=None,
            title="title_json",
        )
        self.data_2.save()

        self.data_3 = Data(
            template=self.template,
            user_id="2",
            dict_content=None,
            title="title_json",
        )
        self.data_3.save()

        self.data_collection = [
            self.data_1,
            self.data_2,
            self.data_3,
        ]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        content = """{
                  "type": "object",
                  "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"}
                  },
                  "required": ["name", "age"]
                }"""

        self.template = Template()
        self.template.user = 1
        self.template.file = SimpleUploadedFile(
            "user2_template.json", "{}".encode("utf-8")
        )
        self.template.content = content
        self.template.hash = ""
        self.template.format = Template.JSON
        self.template.filename = "filename2.json"
        self.template.save()
