""" Authentication tests for TemplateHtmlRendering REST API
"""

from unittest.mock import patch, Mock

from django.test import SimpleTestCase
from rest_framework import status

from core_main_app.components.template_html_rendering import (
    api as template_html_rendering_api,
)

from core_main_app.rest.template_html_rendering import (
    views as template_html_rendering_views,
)
from core_main_app.rest.template_html_rendering.serializers import (
    TemplateHtmlRenderingSerializer,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestTemplateHtmlRenderingListGetPermission(SimpleTestCase):
    """TestTemplateHtmlRenderingListGetPermission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_get(
            template_html_rendering_views.TemplateHtmlRenderingList.as_view(),
            None,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(template_html_rendering_api, "get_all")
    def test_authenticated_returns_http_403(
        self, mock_template_html_rendering_api_get_all
    ):
        """test_authenticated_returns_http_403

        Args:
            mock_template_html_rendering_api_get_all:

        Returns:

        """
        mock_template_html_rendering_api_get_all.return_value = {}

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            template_html_rendering_views.TemplateHtmlRenderingList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(template_html_rendering_api, "get_all")
    def test_staff_returns_http_200(
        self, mock_template_html_rendering_api_get_all
    ):
        """test_staff_returns_http_200

        Args:
            mock_template_html_rendering_api_get_all:

        Returns:

        """
        mock_template_html_rendering_api_get_all.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            template_html_rendering_views.TemplateHtmlRenderingList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTemplateHtmlRenderingListPostPermission(SimpleTestCase):
    """TestTemplateHtmlRenderingListPostPermission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_post(
            template_html_rendering_views.TemplateHtmlRenderingList.as_view(),
            None,
            data={
                "template": 1,
                "list_rendering": "test",
                "detail_list_rendering": "test",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Args:

        Returns:

        """
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            template_html_rendering_views.TemplateHtmlRenderingList.as_view(),
            mock_user,
            data={
                "template": 1,
                "list_rendering": "test",
                "detail_list_rendering": "test",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(TemplateHtmlRenderingSerializer, "save")
    @patch.object(TemplateHtmlRenderingSerializer, "is_valid")
    @patch.object(TemplateHtmlRenderingSerializer, "data")
    def test_staff_returns_http_201(
        self,
        mock_template_html_rendering_serializer_data,
        mock_template_html_rendering_serializer_is_valid,
        mock_template_html_rendering_serializer_save,
    ):
        """test_staff_returns_http_201

        Args:
            mock_template_html_rendering_serializer_data:
            mock_template_html_rendering_serializer_is_valid:
            mock_template_html_rendering_serializer_save:

        Returns:

        """
        mock_template_html_rendering_serializer_save.return_value = None
        mock_template_html_rendering_serializer_is_valid.return_value = True
        mock_template_html_rendering_serializer_data.return_value = {}
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            template_html_rendering_views.TemplateHtmlRenderingList.as_view(),
            mock_user,
            data={
                "template": 1,
                "list_rendering": "test",
                "detail_list_rendering": "test",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestTemplateHtmlRenderingDetailGetPermission(SimpleTestCase):
    """TestTemplateHtmlRenderingDetailGetPermission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_get(
            template_html_rendering_views.TemplateHtmlRenderingDetail.as_view(),
            None,
            param={"pk": 1},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Returns:

        """
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            template_html_rendering_views.TemplateHtmlRenderingDetail.as_view(),
            mock_user,
            param={"pk": 1},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(template_html_rendering_api, "get_by_id")
    @patch.object(TemplateHtmlRenderingSerializer, "data")
    def test_staff_returns_http_200(
        self,
        mock_template_html_rendering_api_get_by_id,
        mock_template_xsl_serializer_data,
    ):
        """test_staff_returns_http_200

        Args:
            mock_template_html_rendering_api_get_by_id:
            mock_template_xsl_serializer_data:

        Returns:

        """
        mock_template_xsl_serializer_data.return_value = {}
        mock_template_html_rendering_api_get_by_id.return_value = Mock()
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            template_html_rendering_views.TemplateHtmlRenderingDetail.as_view(),
            mock_user,
            param={"pk": 1},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTemplateHtmlRenderingDetailPatchPermission(SimpleTestCase):
    """TestTemplateHtmlRenderingDetailPatchPermission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_patch(
            template_html_rendering_views.TemplateHtmlRenderingDetail.as_view(),
            None,
            param={"pk": 1},
            data={
                "template": 1,
                "list_rendering": "test",
                "detail_list_rendering": "test",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Returns:

        """
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            template_html_rendering_views.TemplateHtmlRenderingDetail.as_view(),
            mock_user,
            param={"pk": 1},
            data={
                "template": 1,
                "list_rendering": "test",
                "detail_list_rendering": "test",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(template_html_rendering_api, "get_by_id")
    @patch.object(TemplateHtmlRenderingSerializer, "save")
    @patch.object(TemplateHtmlRenderingSerializer, "is_valid")
    @patch.object(TemplateHtmlRenderingSerializer, "data")
    def test_staff_returns_http_200(
        self,
        mock_template_html_rendering_serializer_data,
        mock_template_html_rendering_serializer_is_valid,
        mock_template_html_rendering_serializer_save,
        mock_template_html_rendering_api_get_by_id,
    ):
        """test_staff_returns_http_200

        Args:
            mock_template_html_rendering_serializer_data:
            mock_template_html_rendering_serializer_is_valid:
            mock_template_html_rendering_serializer_save:
            mock_template_html_rendering_api_get_by_id:

        Returns:

        """
        mock_template_html_rendering_api_get_by_id.return_value = {}
        mock_template_html_rendering_serializer_save.return_value = None
        mock_template_html_rendering_serializer_is_valid.return_value = True
        mock_template_html_rendering_serializer_data.return_value = {}
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            template_html_rendering_views.TemplateHtmlRenderingDetail.as_view(),
            mock_user,
            param={"pk": 1},
            data={
                "list_xslt": 1,
                "default_detail_xslt": 1,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTemplateHtmlRenderingDetailDeletePermission(SimpleTestCase):
    """TestTemplateHtmlRenderingDetailDeletePermission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_delete(
            template_html_rendering_views.TemplateHtmlRenderingDetail.as_view(),
            None,
            param={"pk": 1},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Returns:

        """
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_delete(
            template_html_rendering_views.TemplateHtmlRenderingDetail.as_view(),
            mock_user,
            param={"pk": 1},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(template_html_rendering_api, "get_by_id")
    @patch.object(template_html_rendering_api, "delete")
    def test_staff_returns_http_204(
        self,
        mock_template_html_rendering_api_get_by_id,
        mock_template_html_rendering_api_delete,
    ):
        """test_staff_returns_http_204

        Args:
            mock_template_html_rendering_api_get_by_id:
            mock_template_html_rendering_api_delete:

        Returns:

        """
        mock_template_html_rendering_api_get_by_id.return_value = Mock()
        mock_template_html_rendering_api_delete.return_value = None
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_delete(
            template_html_rendering_views.TemplateHtmlRenderingDetail.as_view(),
            mock_user,
            param={"pk": 1},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
