"""Unit tests for template version manager rest api
"""
from django.test import SimpleTestCase
from mock.mock import patch
from rest_framework import status

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.rest.template_version_manager import views
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestGlobalTemplateVersionManagerList(SimpleTestCase):
    """TestGlobalTemplateVersionManagerList"""

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    @patch.object(TemplateVersionManager, "get_global_version_managers")
    def test_get_all_returns_http_200(self, mock_get_all):
        """test_get_all_returns_http_200

        Args:
            mock_get_all:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_get_all.return_value = []

        # Mock
        response = RequestMock.do_request_get(
            views.GlobalTemplateVersionManagerList.as_view(), mock_user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserTemplateVersionManagerList(SimpleTestCase):
    """TestUserTemplateVersionManagerList"""

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    @patch.object(TemplateVersionManager, "get_all_version_manager_by_user_id")
    def test_get_all_returns_http_200(self, mock_get_all):
        """test_get_all_returns_http_200

        Args:
            mock_get_all:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_get_all.return_value = []

        # Mock
        response = RequestMock.do_request_get(
            views.UserTemplateVersionManagerList.as_view(), mock_user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTemplateVersionManagerDetail(SimpleTestCase):
    """TestTemplateVersionManagerDetail"""

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    @patch.object(TemplateVersionManager, "get_by_id")
    def test_get_returns_http_200_when_data_exists(self, mock_get_by_id):
        """test_get_returns_http_200_when_data_exists

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_get_by_id.return_value = TemplateVersionManager()
        # Mock
        response = RequestMock.do_request_get(
            views.TemplateVersionManagerDetail.as_view(), mock_user, param={"pk": "id"}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(TemplateVersionManager, "get_by_id")
    def test_get_returns_http_404_when_data_not_found(self, mock_get_by_id):
        """test_get_returns_http_404_when_data_not_found

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_get_by_id.side_effect = DoesNotExist("error")

        # Mock
        response = RequestMock.do_request_get(
            views.TemplateVersionManagerDetail.as_view(),
            mock_user,
            param={"pk": "invalid"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
