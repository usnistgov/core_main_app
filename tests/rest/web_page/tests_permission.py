""" Authentication tests for Web Page REST API
"""
from unittest.mock import patch

from django.test import SimpleTestCase
from rest_framework import status

from core_main_app.components.web_page.models import WebPage
from core_main_app.rest.web_page import views as web_page_views
from core_main_app.rest.web_page.serializers import WebPageSerializer
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestWebPageListGetPermission(SimpleTestCase):
    """TestWebPageListGetPermission"""

    @patch("core_main_app.components.web_page.api.get")
    def test_anonymous_returns_http_200(self, web_page_api_get):
        """test_anonymous_returns_http_200

        Args:
            web_page_api_get:

        Returns:

        """
        web_page_api_get.return_value = _get_mock_web_page()

        response = RequestMock.do_request_get(
            web_page_views.WebPageList.as_view(web_page_type="login"), None
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("core_main_app.components.web_page.api.get")
    def test_authenticated_returns_http_200(self, web_page_api_get):
        """test_authenticated_returns_http_200

        Args:
            web_page_api_get:

        Returns:

        """
        web_page_api_get.return_value = _get_mock_web_page()
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            web_page_views.WebPageList.as_view(web_page_type="login"),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("core_main_app.components.web_page.api.get")
    def test_staff_returns_http_200(self, web_page_api_get):
        """test_staff_returns_http_200

        Args:
            web_page_api_get:

        Returns:

        """
        web_page_api_get.return_value = _get_mock_web_page()
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            web_page_views.WebPageList.as_view(web_page_type="login"),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestWebPageListPostPermission(SimpleTestCase):
    """TestWebPageListPostPermission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_post(
            web_page_views.WebPageList.as_view(web_page_type="login"), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Returns:

        """
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            web_page_views.WebPageList.as_view(web_page_type="login"),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_app.components.web_page.api.get")
    @patch.object(WebPageSerializer, "is_valid")
    @patch.object(WebPageSerializer, "save")
    @patch.object(WebPageSerializer, "data")
    def test_staff_returns_http_201(
        self,
        serializer_data,
        serializer_save,
        serializer_is_valid,
        web_page_api_get,
    ):
        """test_staff_returns_http_201

        Args:
            serializer_data:
            serializer_save:
            serializer_is_valid:
            web_page_api_get:

        Returns:

        """
        web_page_api_get.return_value = _get_mock_web_page()
        serializer_data.return_value = True
        serializer_is_valid.return_value = {}
        serializer_save.return_value = None
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            web_page_views.WebPageList.as_view(web_page_type="login"),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestWebPageListDeletePermission(SimpleTestCase):
    """TestWebPageListDeletePermission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_delete(
            web_page_views.WebPageList.as_view(web_page_type="login"), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Returns:

        """
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_delete(
            web_page_views.WebPageList.as_view(web_page_type="login"),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_app.components.web_page.api.delete_by_type")
    @patch.object(WebPageSerializer, "is_valid")
    @patch.object(WebPageSerializer, "save")
    @patch.object(WebPageSerializer, "data")
    def test_staff_returns_http_204(
        self,
        serializer_data,
        serializer_save,
        serializer_is_valid,
        web_page_api_delete_by_type,
    ):
        """test_staff_returns_http_204

        Args:
            serializer_data:
            serializer_save:
            serializer_is_valid:
            web_page_api_delete_by_type:

        Returns:

        """
        web_page_api_delete_by_type.return_value = None
        serializer_data.return_value = True
        serializer_is_valid.return_value = {}
        serializer_save.return_value = None
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_delete(
            web_page_views.WebPageList.as_view(web_page_type="login"),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


def _get_mock_web_page():
    """Returns a Web page"""
    type_default_for_test = 0
    return WebPage(type=type_default_for_test, content="web page")
