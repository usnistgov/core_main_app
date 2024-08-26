""" Fixtures file for Templates html rendering
"""

from django.core.files.uploadedfile import SimpleUploadedFile

from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.template_html_rendering.models import (
    TemplateHtmlRendering,
)
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)


class TemplateHtmlRenderingFixtures(FixtureInterface):
    """Access Control Data fixture"""

    data_1 = None
    data_2 = None
    data_3 = None
    template_html_rendering_1 = None
    template_html_rendering_2 = None
    template_html_rendering_3 = None
    template_1 = None
    template_2 = None
    template_3 = None
    template_json_1 = None
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
        self.template_1 = Template(
            content=xsd,
            _hash="user1_template_hash",
            filename="user1_template.xsd",
            file=SimpleUploadedFile("user1_template.xsd", xsd.encode("utf-8")),
            user="1",
            _cls="Template_1",
        )
        self.template_1.save()

        self.template_2 = Template(
            content=xsd,
            _hash="user2_template_hash",
            filename="user2_template.xsd",
            file=SimpleUploadedFile("user2_template.xsd", xsd.encode("utf-8")),
            user="2",
            _cls="Template_2",
        )
        self.template_2.save()

        self.template_3 = Template(
            content=xsd,
            _hash="user3_template_hash",
            filename="user3_template.xsd",
            file=SimpleUploadedFile("user3_template.xsd", xsd.encode("utf-8")),
            user="2",
            _cls="Template_3",
        )
        self.template_3.save()

        self.template_json_1 = Template()
        self.template_json_1.user = "2"
        self.template_json_1.format = Template.JSON
        self.template_json_1.file = SimpleUploadedFile(
            "user2_template.json", "{}".encode("utf-8")
        )
        self.template_json_1.save()

        self.template_html_rendering_1 = TemplateHtmlRendering(
            template=self.template_1,
            list_rendering="<b>Title:<b/>{{dict_content.root.title}}",
            detail_rendering="detail_rendering_1",
        )
        self.template_html_rendering_1.save()

        self.template_html_rendering_2 = TemplateHtmlRendering(
            template=self.template_2
        )
        self.template_html_rendering_2.save()

        self.template_html_rendering_3 = TemplateHtmlRendering(
            template=self.template_json_1,
            list_rendering="<b>Title:<b/>{{dict_content.root.title}}",
            detail_rendering="detail_rendering_json_1",
        )
        self.template_html_rendering_3.save()

        self.data_1 = Data(
            template=self.template_1,
            user_id="1",
            title="title",
            content="<root><title>CDCS</title></root>",
        )
        self.data_1.save()
        self.data_2 = Data(
            template=self.template_3,
            user_id="1",
            title="title2",
            xml_content="<root></root>",
        )
        self.data_2.save()

        self.data_3 = Data(
            template=self.template_json_1,
            user_id="2",
            title="data_json",
            content='{"root": {"title": "CDCS"}}',
        )
        self.data_3.save()

        self.template_collection = [
            self.template_html_rendering_1,
            self.template_html_rendering_2,
            self.template_html_rendering_3,
            self.template_1,
            self.template_2,
            self.template_3,
            self.template_json_1,
            self.data_1,
            self.data_2,
            self.data_3,
        ]
