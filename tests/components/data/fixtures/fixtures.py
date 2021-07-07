""" Fixtures files for Data
"""
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.workspace.models import Workspace
from core_main_app.components.xsl_transformation.models import XslTransformation
from core_main_app.components.workspace import api as workspace_api
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
        ).save()
        self.data_2 = Data(
            template=self.template, user_id="2", dict_content=None, title="title2"
        ).save()
        self.data_3 = Data(
            template=self.template, user_id="1", dict_content=None, title="title3"
        ).save()
        self.data_collection = [self.data_1, self.data_2, self.data_3]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        template.content = xsd
        template.hash = ""
        template.filename = "filename"
        self.template = template.save()


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
        ).save()
        self.data_2 = Data(
            template=self.template, user_id="2", dict_content=content_2, title="title2"
        ).save()
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

        self.data_1 = Data(template=self.template, title="Data 1", user_id="1").save()
        self.data_2 = Data(template=self.template, title="Data 2", user_id="2").save()
        self.data_3 = Data(
            template=self.template,
            title="Data 3",
            user_id="1",
            workspace=self.workspace_1.id,
            dict_content=content,
        ).save()
        self.data_4 = Data(
            template=self.template,
            title="DataDoubleTitle",
            user_id="2",
            workspace=self.workspace_2.id,
        ).save()
        self.data_5 = Data(
            template=self.template,
            title="DataDoubleTitle",
            user_id="1",
            workspace=self.workspace_1.id,
        ).save()
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
        template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        template.content = xsd
        template.hash = ""
        template.filename = "filename"
        self.template = template.save()

    def generate_workspace(self):
        """Generate the workspaces.

        Returns:

        """
        self.workspace_1 = Workspace(
            title="Workspace 1", owner="1", read_perm_id="1", write_perm_id="1"
        ).save()
        self.workspace_2 = Workspace(
            title="Workspace 2", owner="2", read_perm_id="2", write_perm_id="2"
        ).save()

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
        except Exception as e:
            print(str(e))


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
        template1 = Template()
        template2 = Template()
        template3 = Template()
        template4 = Template()
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
        template1.content = xsd1
        template1.hash = ""
        template1.filename = "filename"
        template2.content = xsd2
        template2.hash = ""
        template2.filename = "filename"
        template3.content = xsd3
        template3.hash = ""
        template3.filename = "filename"
        template4.content = xsd4
        template4.hash = ""
        template4.filename = "filename"
        self.template_1 = template1.save()
        self.template_2 = template2.save()
        self.template_3 = template3.save()
        self.template_4 = template4.save()

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
        xsl_transformation = XslTransformation(
            name="xsl_transformation",
            filename="xsl_transformation.xsl",
            content=content,
        )

        self.xsl_transformation = xsl_transformation.save()
