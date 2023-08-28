""" Fixtures files for TemplateXslRendering
"""

from core_main_app.components.template.models import Template
from core_main_app.components.template_xsl_rendering.models import (
    TemplateXslRendering,
)
from core_main_app.components.xsl_transformation.models import (
    XslTransformation,
)
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)


class TemplateXslRenderingFixtures(FixtureInterface):
    """TemplateXslRendering fixtures"""

    template_1 = None
    template_2 = None
    template_3 = None
    template_xsl_rendering_1 = None
    template_xsl_rendering_2 = None
    xsl_transformation_1 = None
    xsl_transformation_2 = None
    xsl_transformation_3 = None
    template_xsl_rendering_collection = None
    xsl_transformation_collection = None

    def insert_data(self):
        """Insert a set of TemplateXslRendering and XslTransformation.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template_xsl_rendering_collection()
        self.generate_xsl_transformation_collection()

    def generate_template_xsl_rendering_collection(self):
        """Generate a TemplateXslRendering collection.

        Returns:

        """
        self.template_1 = Template(
            filename="template_1.xsd", content="content1", _hash="hash1"
        )
        self.template_1.save()
        self.template_2 = Template(
            filename="template_2.xsd", content="content2", _hash="hash2"
        )
        self.template_2.save()
        self.template_3 = Template(
            filename="template_3.xsd", content="content3", _hash="hash3"
        )
        self.template_3.save()
        self.template_xsl_rendering_1 = TemplateXslRendering(
            template=self.template_1
        )
        self.template_xsl_rendering_1.save()
        self.xsl_transformation_3 = XslTransformation(
            name="xsl_transformation_3",
            filename="xsl_transformation_3",
            content="content_3",
        )
        self.xsl_transformation_3.save()

        self.template_xsl_rendering_2 = TemplateXslRendering(
            template=self.template_2,
            default_detail_xslt=self.xsl_transformation_3,
        )
        self.template_xsl_rendering_2.save()
        self.template_xsl_rendering_2.list_detail_xslt.set(
            [self.xsl_transformation_3]
        )

        self.template_xsl_rendering_collection = [
            self.template_xsl_rendering_1,
            self.template_xsl_rendering_2,
        ]

    def generate_xsl_transformation_collection(self):
        """Generate a XslTransformation collection.

        Returns:

        """
        self.xsl_transformation_1 = XslTransformation(
            name="xsl_transformation_1",
            filename="xsl_transformation_1",
            content="content1",
        )
        self.xsl_transformation_1.save()
        self.xsl_transformation_2 = XslTransformation(
            name="xsl_transformation_2",
            filename="xsl_transformation_2",
            content="content_2",
        )
        self.xsl_transformation_2.save()

        self.xsl_transformation_collection = [
            self.xsl_transformation_1,
            self.xsl_transformation_2,
        ]
