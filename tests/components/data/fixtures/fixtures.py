""" Fixtures files for Data
"""
from django.core.files.uploadedfile import SimpleUploadedFile

from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.workspace import api as workspace_api
from core_main_app.components.workspace.models import Workspace
from core_main_app.components.xsl_transformation.models import XslTransformation
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface


class DataFixtures(FixtureInterface):
    """Data fixtures"""

    data_1 = None
    data_2 = None
    data_3 = None
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
        # NOTE: no xml_content to avoid using unsupported GridFS mock
        self.data_1 = Data(
            template=self.template, user_id="1", dict_content=None, title="title"
        )
        self.data_1.save()
        self.data_2 = Data(
            template=self.template, user_id="2", dict_content=None, title="title2"
        )
        self.data_2.save()
        self.data_3 = Data(
            template=self.template, user_id="1", dict_content=None, title="title3"
        )
        self.data_3.save()
        self.data_collection = [self.data_1, self.data_2, self.data_3]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        self.template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        self.template.content = xsd
        self.template.hash = ""
        self.template.filename = "filename"
        self.template.save()


class QueryDataFixtures(DataFixtures):
    """Data fixtures"""

    def generate_data_collection(self):
        """Generate a Data collection.

        Returns:

        """
        content_1 = {
            "root": {
                "element": "value",
                "list": [{"element_list_1": 1}, {"element_list_2": 2}],
                "complex": {"child1": "test", "child2": 0},
            }
        }
        content_2 = {"root": {"element": "value2"}}
        # NOTE: no xml_content to avoid using unsupported GridFS mock
        self.data_1 = Data(
            template=self.template, user_id="1", dict_content=content_1, title="title"
        )
        self.data_1.save()
        self.data_2 = Data(
            template=self.template, user_id="2", dict_content=content_2, title="title2"
        )
        self.data_2.save()
        self.data_collection = [self.data_1, self.data_2]


class AccessControlDataFixture(FixtureInterface):
    """Access Control Data fixture"""

    USER_1_NO_WORKSPACE = 0
    USER_2_NO_WORKSPACE = 1
    USER_1_WORKSPACE_1 = 2
    USER_2_WORKSPACE_2 = 3

    template = None
    workspace_1 = None
    workspace_2 = None
    data_collection = None
    data_1 = None
    data_2 = None
    data_3 = None
    data_4 = None
    data_5 = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_workspace()
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a Data collection.

        Returns:

        """

        content = {"root": {"element": "value2"}}

        self.data_1 = Data(template=self.template, title="Data 1", user_id="1")
        self.data_1.save()
        self.data_2 = Data(template=self.template, title="Data 2", user_id="2")
        self.data_2.save()
        self.data_3 = Data(
            template=self.template,
            title="Data 3",
            user_id="1",
            workspace=self.workspace_1,
            dict_content=content,
        )
        self.data_3.save()
        self.data_4 = Data(
            template=self.template,
            title="DataDoubleTitle",
            user_id="2",
            workspace=self.workspace_2,
        )
        self.data_4.save()
        self.data_5 = Data(
            template=self.template,
            title="DataDoubleTitle",
            user_id="1",
            workspace=self.workspace_1,
        )
        self.data_5.save()
        self.data_collection = [
            self.data_1,
            self.data_2,
            self.data_3,
            self.data_4,
            self.data_5,
        ]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        self.template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        self.template.content = xsd
        self.template.hash = ""
        self.template.filename = "filename"
        self.template.save()

    def generate_workspace(self):
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

    def generate_workspace_with_perm(self):
        """Generate the workspaces and the perm object.

        Returns:

        """
        try:
            self.workspace_1 = workspace_api.create_and_save("Workspace 1")
            self.workspace_2 = workspace_api.create_and_save("Workspace 2")
            self.data_3.workspace = self.workspace_1
            self.data_4.workspace = self.workspace_2
            self.data_5.workspace = self.workspace_1
        except Exception as exception:
            print(str(exception))


class AccessControlDataFixture2(FixtureInterface):
    """Access Control Data fixture
    - User1: 1 private data
    - User2: 1 data in workspace 1
    - User3: 1 private data and 1 data in workspace 1
    """

    template = None
    workspace_1 = None
    data_collection = None
    data_1 = None
    data_2 = None
    data_3_1 = None
    data_3_2 = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_workspace()
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a Data collection.

        Returns:

        """

        content = {"root": {"element": "value2"}}

        self.data_1 = Data(
            template=self.template, title="Data 1", user_id="1", dict_content=content
        )
        self.data_1.save()
        self.data_2 = Data(
            template=self.template,
            title="Data 2",
            user_id="2",
            workspace=self.workspace_1,
        )
        self.data_2.save()
        self.data_3_1 = Data(
            template=self.template,
            title="Data 3.1",
            user_id="3",
            dict_content=content,
        )
        self.data_3_1.save()
        self.data_3_2 = Data(
            template=self.template,
            title="Data 3.2",
            user_id="3",
            workspace=self.workspace_1,
            dict_content=content,
        )
        self.data_3_2.save()
        self.data_collection = [
            self.data_1,
            self.data_2,
            self.data_3_1,
            self.data_3_2,
        ]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        self.template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        self.template.content = xsd
        self.template.hash = ""
        self.template.filename = "filename"
        self.template.save()

    def generate_workspace(self):
        """Generate the workspaces.

        Returns:

        """
        self.workspace_1 = Workspace(
            title="Workspace 1", owner=None, read_perm_id="1", write_perm_id="1"
        )
        self.workspace_1.save()


class AccessControlDataFullTextSearchFixture(FixtureInterface):
    """Access Control Data fixture
    - User1: 1 private data
    - User2: 1 data in workspace 1
    - User3: 1 private data and 1 data in workspace 1
    """

    template = None
    workspace_1 = None
    data_collection = None
    data_1 = None
    data_2 = None
    data_3_1 = None
    data_3_2 = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_workspace()
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a Data collection.

        Returns:

        """

        # _1: user1 is unique and private, value1 is also in _2
        xml_content_1 = "<root><element>user1</element><element>value1</element></root>"
        # _2: value1 is common to _1 and _2
        xml_content_2 = "<root><element>value1</element></root>"
        # _3_1: value31 is unique and private
        xml_content_3_1 = "<root><element>value31</element></root>"
        # _3_2: value32 is unique
        xml_content_3_2 = "<root><element>value32</element></root>"

        self.data_1 = Data(
            template=self.template,
            title="Data 1",
            user_id="1",
            xml_content=xml_content_1,
        )
        self.data_1.convert_and_save()
        self.data_2 = Data(
            template=self.template,
            title="Data 2",
            user_id="2",
            xml_content=xml_content_2,
            workspace=self.workspace_1,
        )
        self.data_2.convert_and_save()
        self.data_3_1 = Data(
            template=self.template,
            title="Data 3.1",
            user_id="3",
            xml_content=xml_content_3_1,
        )
        self.data_3_1.convert_and_save()
        self.data_3_2 = Data(
            template=self.template,
            title="Data 3.2",
            user_id="3",
            workspace=self.workspace_1,
            xml_content=xml_content_3_2,
        )
        self.data_3_2.convert_and_save()
        self.data_collection = [
            self.data_1,
            self.data_2,
            self.data_3_1,
            self.data_3_2,
        ]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        self.template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        self.template.content = xsd
        self.template.hash = ""
        self.template.filename = "filename"
        self.template.save()

    def generate_workspace(self):
        """Generate the workspaces.

        Returns:

        """
        self.workspace_1 = Workspace(
            title="Workspace 1", owner=None, read_perm_id="1", write_perm_id="1"
        )
        self.workspace_1.save()


class DataMigrationFixture(FixtureInterface):
    """Data Template Fixture"""

    template_1 = None
    template_2 = None
    template_3 = None
    template_4 = None
    data_collection = None
    data_1 = None
    data_2 = None
    data_3 = None
    data_4 = None
    data_5 = None
    xsl_transformation = None
    xsl_transformation_2 = None

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
        self.data_1 = Data(template=self.template_1, title="Data 1", user_id="1")
        self.data_1.xml_content = '<root xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> \
                                    <test>test</test> \
                                  </root>'
        self.data_1.save()

        self.data_2 = Data(template=self.template_1, title="Data 2", user_id="1")
        self.data_2.xml_content = '<root xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> \
                                    <test>test</test> \
                                  </root>'
        self.data_2.save()

        self.data_3 = Data(template=self.template_2, title="Data 3", user_id="1")
        self.data_3.xml_content = '<root xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> \
                                    <test>test</test> \
                                  </root>'

        self.data_3.save()

        self.data_4 = Data(template=self.template_3, title="Data4", user_id="1")
        self.data_4.xml_content = '<root xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> \
                                    <other>test</other> \
                                  </root>'
        self.data_4.save()

        self.data_5 = Data(template=self.template_3, title="Data5", user_id="1")
        self.data_5.xml_content = '<root xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> \
                                    <other>test</other> \
                                  </root>'
        self.data_5.save()

        self.data_collection = [
            self.data_1,
            self.data_2,
            self.data_3,
            self.data_4,
            self.data_5,
        ]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        self.template_1 = Template()
        self.template_2 = Template()
        self.template_3 = Template()
        self.template_4 = Template()
        xsd1 = '<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"> \
                <xsd:element name="root" type="simpleString"/> \
                <xsd:complexType name="simpleString"> \
                    <xsd:sequence> \
                    <xsd:element name="test" type="xsd:string"/></xsd:sequence> \
                </xsd:complexType> \
            </xsd:schema>'
        xsd2 = '<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"> \
                <xsd:element name="root" type="simpleString"/> \
                <xsd:complexType name="simpleString"> \
                    <xsd:sequence> \
                    <xsd:element name="test" type="xsd:string"/></xsd:sequence> \
                </xsd:complexType> \
            </xsd:schema>'
        xsd3 = '<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"> \
                <xsd:element name="root" type="simpleString"/> \
                <xsd:complexType name="simpleString"> \
                    <xsd:sequence> \
                    <xsd:element name="other" type="xsd:string"/></xsd:sequence> \
                </xsd:complexType> \
            </xsd:schema>'
        xsd4 = '<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"> \
                        <xsd:element name="root" type="simpleString" /> \
                        <xsd:complexType name="simpleString"> \
                            <xsd:sequence> \
                                <xsd:element name="test" type="xsd:string"/> \
                                <xsd:element name="element" type="xsd:string"/> \
                            </xsd:sequence> \
                        </xsd:complexType> \
                </xsd:schema>'
        self.template_1.content = xsd1
        self.template_1.hash = ""
        self.template_1.filename = "filename"
        self.template_2.content = xsd2
        self.template_2.hash = ""
        self.template_2.filename = "filename"
        self.template_3.content = xsd3
        self.template_3.hash = ""
        self.template_3.filename = "filename"
        self.template_4.content = xsd4
        self.template_4.hash = ""
        self.template_4.filename = "filename"
        self.template_1.save_template()
        self.template_2.save_template()
        self.template_3.save_template()
        self.template_4.save_template()

    def generate_xslt(self):
        """Generate xsl transformation .

        Returns:

        """

        content = '<?xml version="1.0" encoding="UTF-8"?> \
                <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"> \
                    <xsl:template match="@* | node()">   \
                        <xsl:copy> \
                            <xsl:apply-templates select="@* | node()"/> \
                        </xsl:copy> \
                    </xsl:template> \
                    <xsl:template match="test"> \
                        <xsl:copy-of select="."/> \
                        <element>new_element</element> \
                    </xsl:template> \
                </xsl:stylesheet>'
        self.xsl_transformation = XslTransformation(
            name="xsl_transformation",
            filename="xsl_transformation.xsl",
            file=SimpleUploadedFile(
                "xsl_transformation.xsl", content=content.encode("utf-8")
            ),
        )

        self.xsl_transformation.save()
