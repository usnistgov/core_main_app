""" Tests View Data utils
"""
from unittest import TestCase

from core_main_app.components.data.models import Data
from core_main_app.utils.view_builders.data import (
    _get_field,
    xslt_selector,
)
from tests.components.template_xsl_rendering.fixtures.fixtures import (
    TemplateXslRenderingFixtures,
)
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)

fixture_template_rendering = TemplateXslRenderingFixtures()


class TestGetField(TestCase):
    """Test _get_field"""

    def setUp(self) -> None:
        self.title = "test"

    def test_page_title_set_when_when_in_data(self):
        """test_page_title_set_when_when_in_data

        Returns:

        """
        # Arrange
        data = Data(title=self.title)
        # Act
        data_title = _get_field(data, "title")
        # Assert
        self.assertEqual(data_title, self.title)

    def test_page_title_empty_when_not_set_in_data(self):
        """test_page_title_None_when_not_when_in_data

        Returns:

        """
        # Arrange
        data = Data()
        # Act
        data_title = _get_field(data, "title")
        # Assert
        self.assertEqual(data_title, "")

    def test_page_title_None_when_not_in_dict(self):
        """test_page_title_None_when_not_in_dict

        Returns:

        """
        # Arrange
        data = {}
        # Act
        data_title = _get_field(data, "title")
        # Assert
        self.assertEqual(data_title, None)

    def test_page_title_set_when_in_dict(self):
        """test_page_title_set_when_in_dict

        Returns:

        """
        # Arrange
        data = {"title": self.title}
        # Act
        data_title = _get_field(data, "title")
        # Assert
        self.assertEqual(data_title, self.title)

    def test_page_title_None_when_not_data_is_None(self):
        """test_page_title_None_when_not_data_is_None

        Returns:

        """
        # Arrange
        data = None
        # Act
        data_title = _get_field(data, "title")
        # Assert
        self.assertEqual(data_title, None)

    def test_get_bad_field_return_None(self):
        """test_get_bad_field_return_None

        Returns:

        """
        # Arrange
        data = {"title": self.title}
        # Act
        data_title = _get_field(data, "bad")
        # Assert
        self.assertEqual(data_title, None)


class TestXsltSelector(IntegrationBaseTestCase):
    """Test raw_xml_to_dict"""

    fixture = fixture_template_rendering

    def test_xslt_selector_returns_default_config_when_template_xsl_rendering_is_not_set(
        self,
    ):
        """test_get_default_config_when_template_xsl_rendering_is_not_set

        Returns:

        """
        # Arrange # Act
        (
            display_xslt_selector,
            template_xsl_rendering,
            xsl_transformation_id,
        ) = xslt_selector(self.fixture.template_3.id)
        # Assert
        self.assertEqual(display_xslt_selector, False)
        self.assertEqual(template_xsl_rendering, None)
        self.assertEqual(xsl_transformation_id, None)

    def test_xslt_selector_with_only_template_xsl_rendering(self):
        """test_page_title_set_when_when_in_data

        Returns:

        """
        # Arrange # Act
        (
            display_xslt_selector,
            template_xsl_rendering,
            xsl_transformation_id,
        ) = xslt_selector(self.fixture.template_1.id)
        # Assert
        self.assertEqual(display_xslt_selector, False)
        self.assertEqual(
            template_xsl_rendering, self.fixture.template_xsl_rendering_1
        )
        self.assertEqual(xsl_transformation_id, None)

    def test_xslt_selector_returns_correct_config(self):
        """test_xslt_selector_returns_correct_config

        Returns:

        """
        # Arrange # Act
        (
            display_xslt_selector,
            template_xsl_rendering,
            xsl_transformation_id,
        ) = xslt_selector(self.fixture.template_2.id)
        # Assert
        self.assertEqual(display_xslt_selector, False)
        self.assertEqual(
            template_xsl_rendering, self.fixture.template_xsl_rendering_2
        )
        self.assertEqual(
            xsl_transformation_id, self.fixture.xsl_transformation_3.id
        )
