""" Test XSD Flattener
"""
from unittest import TestCase

from django.test.utils import override_settings
from django.urls import reverse
from mock.mock import patch

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.template import api as template_api
from core_main_app.components.template.models import Template
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from core_main_app.utils.xsd_flattener.xsd_flattener_database_url import (
    XSDFlattenerDatabaseOrURL,
    XSDFlattenerRequestsURL,
)


class TestXSDFlattenerDatabaseUrl(TestCase):
    """TestXSDFlattenerDatabaseUrl"""

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch.object(XSDFlattenerRequestsURL, "get_dependency_content")
    def test_url_not_recognized_use_xsd_flattener_url(
        self, mock_get_dependency_content
    ):
        """test url not recognized use xsd flattener url

        Args:
            mock_get_dependency_content:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        xml_string = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:include schemaLocation="http://dummy.com/download?id=1234"/></xs:schema>'
        )
        dependency = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="test"/></xs:schema>'
        )
        mock_get_dependency_content.return_value = dependency

        # Act
        flattener = XSDFlattenerDatabaseOrURL(xml_string, request=mock_request)
        flat_string = flattener.get_flat()

        # Assert
        self.assertTrue('<xs:element name="test"/>' in flat_string)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch.object(template_api, "get_by_id")
    def test_url_recognized_use_database(self, mock_get):
        """test url recognized use database

        Args:
            mock_get:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        url_template_download = reverse(
            "core_main_app_rest_template_download", kwargs={"pk": "pk"}
        )
        xml_string = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            f'<xs:include schemaLocation="http://dummy.com{url_template_download}?id=1234"/>'
            "</xs:schema>"
        )
        dependency = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="test"/></xs:schema>'
        )
        mock_get.return_value = Template(content=dependency)

        # Act
        flattener = XSDFlattenerDatabaseOrURL(xml_string, request=mock_request)
        flat_string = flattener.get_flat()

        # Assert
        self.assertTrue('<xs:element name="test"/>' in flat_string)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch.object(template_api, "get_by_id")
    @patch.object(XSDFlattenerRequestsURL, "get_dependency_content")
    def test_url_recognized_template_does_not_exist(
        self, mock_get_dependency_content, mock_get
    ):
        """test url recognized template does not exist

        Args:
            mock_get_dependency_content:
            mock_get:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)

        xml_string = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:include schemaLocation="http://dummy.com{0}?id=1234"/>'
            "</xs:schema>"
        )
        dependency = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="test"/></xs:schema>'
        )
        mock_get_dependency_content.return_value = dependency
        mock_get.side_effect = DoesNotExist("Error")

        # Act
        flattener = XSDFlattenerDatabaseOrURL(xml_string, request=mock_request)
        flat_string = flattener.get_flat()

        # Assert
        self.assertTrue('<xs:element name="test"/>' in flat_string)
