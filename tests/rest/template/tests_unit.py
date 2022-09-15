"""Unit tests for template rest api
"""
from django.test import SimpleTestCase
from mock.mock import patch
from rest_framework import status

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.template.models import Template

from core_main_app.rest.template import views as template_rest_views
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
import core_main_app.components.template.api as template_api


class TestTemplateDownload(SimpleTestCase):
    """Test Template Download"""

    def setUp(self):
        """setUp"""

        super().setUp()

    @patch.object(template_api, "get_by_id")
    def test_get_returns_http_404_when_data_not_found(
        self, mock_template_api_get_by_id
    ):
        """test_get_returns_http_404_when_data_not_found"""

        # Arrange
        mock_user = create_mock_user("1")
        mock_template_api_get_by_id.side_effect = DoesNotExist("error")

        # Mock
        response = RequestMock.do_request_get(
            template_rest_views.TemplateDownload.as_view(), mock_user, param={"pk": "1"}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(template_api, "get_by_id")
    def test_get_returns_http_200_when_data_found(self, mock_template_api_get_by_id):
        """test_get_returns_http_200_when_data_found"""

        # Arrange
        mock_user = create_mock_user("1")
        mock_template = _get_template()
        mock_template_api_get_by_id.return_value = mock_template

        # Mock
        response = RequestMock.do_request_get(
            template_rest_views.TemplateDownload.as_view(), mock_user, param={"pk": "1"}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(template_api, "get_by_id")
    def test_get_returns_http_400_when_data_not_well_formatted(
        self, mock_template_api_get_by_id
    ):
        """test_get_returns_http_400_when_data_not_well_formatted"""

        # Arrange
        mock_user = create_mock_user("1")
        mock_template = Template()
        mock_template.content = "/test"
        mock_template_api_get_by_id.return_value = mock_template

        # Mock
        response = RequestMock.do_request_get(
            template_rest_views.TemplateDownload.as_view(),
            mock_user,
            param={"pk": "1"},
            data={"pretty_print": "true"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(template_api, "get_by_id")
    def test_get_without_pretty_print_returns_data(self, mock_template_api_get_by_id):
        """test_get_without_pretty_print_returns_data"""

        # Arrange
        mock_user = create_mock_user("1")
        mock_template = _get_template()
        mock_template_api_get_by_id.return_value = mock_template
        expected_value = b'<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="tag"></xs:element></xs:schema>'
        # Mock
        response = RequestMock.do_request_get(
            template_rest_views.TemplateDownload.as_view(),
            mock_user,
            param={"pk": "1"},
            data={"pretty_print": "false"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected_value)

    @patch.object(template_api, "get_by_id")
    def test_get_with_pretty_print_returns_formatted_data(
        self, mock_template_api_get_by_id
    ):
        """test_get_with_pretty_print_returns_formatted_data"""

        # Arrange
        mock_user = create_mock_user("1")
        mock_template = _get_template()
        mock_template_api_get_by_id.return_value = mock_template
        expected_value = b'<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">\n  <xs:element name="tag"/>\n</xs:schema>\n'

        # Mock
        response = RequestMock.do_request_get(
            template_rest_views.TemplateDownload.as_view(),
            mock_user,
            param={"pk": "1"},
            data={"pretty_print": "true"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected_value)


def _get_template():
    """_get_template

    Args:

    Returns:
    """
    template = Template()
    template.id = 1
    template.filename = "test"
    xsd = (
        '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
        '<xs:element name="tag"></xs:element></xs:schema>'
    )
    template.content = xsd
    return template
