""" Authentication tests for TemplateXSLRendering REST API
"""
from bson import ObjectId
from django.test import SimpleTestCase
from mock import patch, Mock
from rest_framework import status

from core_main_app.components.template_xsl_rendering import (
    api as template_xsl_rendering_api,
)
from core_main_app.rest.template_xsl_rendering import (
    views as template_xsl_rendering_views,
)
from core_main_app.rest.template_xsl_rendering.serializers import (
    TemplateXslRenderingSerializer,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestTemplateXslRenderingListGetPermission(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(
            template_xsl_rendering_views.TemplateXslRenderingList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(template_xsl_rendering_api, "get_all")
    def test_authenticated_returns_http_200(
        self, mock_template_xsl_rendering_api_get_all
    ):
        mock_template_xsl_rendering_api_get_all.return_value = {}

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            template_xsl_rendering_views.TemplateXslRenderingList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(template_xsl_rendering_api, "get_all")
    def test_staff_returns_http_200(self, mock_template_xsl_rendering_api_get_all):
        mock_template_xsl_rendering_api_get_all.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            template_xsl_rendering_views.TemplateXslRenderingList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTemplateXslRenderingListPostPermission(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_post(
            template_xsl_rendering_views.TemplateXslRenderingList.as_view(),
            None,
            data={
                "template": str(ObjectId()),
                "list_xslt": str(ObjectId()),
                "default_detail_xslt": str(ObjectId()),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(TemplateXslRenderingSerializer, "save")
    @patch.object(TemplateXslRenderingSerializer, "is_valid")
    @patch.object(TemplateXslRenderingSerializer, "data")
    def test_authenticated_returns_http_201(
        self,
        mock_template_xsl_rendering_serializer_data,
        mock_template_xsl_rendering_serializer_is_valid,
        mock_template_xsl_rendering_serializer_save,
    ):
        mock_template_xsl_rendering_serializer_save.return_value = None
        mock_template_xsl_rendering_serializer_is_valid.return_value = True
        mock_template_xsl_rendering_serializer_data.return_value = {}
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            template_xsl_rendering_views.TemplateXslRenderingList.as_view(),
            mock_user,
            data={
                "template": str(ObjectId()),
                "list_xslt": str(ObjectId()),
                "default_detail_xslt": str(ObjectId()),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(TemplateXslRenderingSerializer, "save")
    @patch.object(TemplateXslRenderingSerializer, "is_valid")
    @patch.object(TemplateXslRenderingSerializer, "data")
    def test_staff_returns_http_201(
        self,
        mock_template_xsl_rendering_serializer_data,
        mock_template_xsl_rendering_serializer_is_valid,
        mock_template_xsl_rendering_serializer_save,
    ):
        mock_template_xsl_rendering_serializer_save.return_value = None
        mock_template_xsl_rendering_serializer_is_valid.return_value = True
        mock_template_xsl_rendering_serializer_data.return_value = {}
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            template_xsl_rendering_views.TemplateXslRenderingList.as_view(),
            mock_user,
            data={
                "template": str(ObjectId()),
                "list_xslt": str(ObjectId()),
                "default_detail_xslt": str(ObjectId()),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestTemplateXslRenderingDetailGetPermission(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(
            template_xsl_rendering_views.TemplateXslRenderingDetail.as_view(),
            None,
            param={"pk": str(ObjectId())},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(template_xsl_rendering_api, "get_by_id")
    @patch.object(TemplateXslRenderingSerializer, "data")
    def test_authenticated_returns_http_200(
        self,
        mock_template_xsl_rendering_api_get_by_id,
        mock_template_xsl_serializer_data,
    ):
        mock_template_xsl_serializer_data.return_value = {}
        mock_template_xsl_rendering_api_get_by_id.return_value = Mock()
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            template_xsl_rendering_views.TemplateXslRenderingDetail.as_view(),
            mock_user,
            param={"pk": str(ObjectId())},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(template_xsl_rendering_api, "get_by_id")
    @patch.object(TemplateXslRenderingSerializer, "data")
    def test_staff_returns_http_200(
        self,
        mock_template_xsl_rendering_api_get_by_id,
        mock_template_xsl_serializer_data,
    ):
        mock_template_xsl_serializer_data.return_value = {}
        mock_template_xsl_rendering_api_get_by_id.return_value = Mock()
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            template_xsl_rendering_views.TemplateXslRenderingDetail.as_view(),
            mock_user,
            param={"pk": str(ObjectId())},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTemplateXslRenderingDetailPatchPermission(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_patch(
            template_xsl_rendering_views.TemplateXslRenderingDetail.as_view(),
            None,
            param={"pk": str(ObjectId())},
            data={"list_xslt": str(ObjectId()), "default_detail_xslt": str(ObjectId())},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(template_xsl_rendering_api, "get_by_id")
    @patch.object(TemplateXslRenderingSerializer, "save")
    @patch.object(TemplateXslRenderingSerializer, "is_valid")
    @patch.object(TemplateXslRenderingSerializer, "data")
    def test_authenticated_returns_http_200(
        self,
        mock_template_xsl_rendering_serializer_data,
        mock_template_xsl_rendering_serializer_is_valid,
        mock_template_xsl_rendering_serializer_save,
        mock_template_xsl_rendering_api_get_by_id,
    ):
        mock_template_xsl_rendering_api_get_by_id.return_value = {}
        mock_template_xsl_rendering_serializer_save.return_value = None
        mock_template_xsl_rendering_serializer_is_valid.return_value = True
        mock_template_xsl_rendering_serializer_data.return_value = {}
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            template_xsl_rendering_views.TemplateXslRenderingDetail.as_view(),
            mock_user,
            param={"pk": str(ObjectId())},
            data={"list_xslt": str(ObjectId()), "default_detail_xslt": str(ObjectId())},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(template_xsl_rendering_api, "get_by_id")
    @patch.object(TemplateXslRenderingSerializer, "save")
    @patch.object(TemplateXslRenderingSerializer, "is_valid")
    @patch.object(TemplateXslRenderingSerializer, "data")
    def test_staff_returns_http_200(
        self,
        mock_template_xsl_rendering_serializer_data,
        mock_template_xsl_rendering_serializer_is_valid,
        mock_template_xsl_rendering_serializer_save,
        mock_template_xsl_rendering_api_get_by_id,
    ):
        mock_template_xsl_rendering_api_get_by_id.return_value = {}
        mock_template_xsl_rendering_serializer_save.return_value = None
        mock_template_xsl_rendering_serializer_is_valid.return_value = True
        mock_template_xsl_rendering_serializer_data.return_value = {}
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            template_xsl_rendering_views.TemplateXslRenderingDetail.as_view(),
            mock_user,
            param={"pk": str(ObjectId())},
            data={
                "list_xslt": str(ObjectId()),
                "default_detail_xslt" "": str(ObjectId()),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTemplateXslRenderingDetailDeletePermission(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_delete(
            template_xsl_rendering_views.TemplateXslRenderingDetail.as_view(),
            None,
            param={"pk": str(ObjectId())},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(template_xsl_rendering_api, "get_by_id")
    @patch.object(template_xsl_rendering_api, "delete")
    def test_authenticated_returns_http_204(
        self,
        mock_template_xsl_rendering_api_get_by_id,
        mock_template_xsl_rendering_api_delete,
    ):
        mock_template_xsl_rendering_api_get_by_id.return_value = Mock()
        mock_template_xsl_rendering_api_delete.return_value = None
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_delete(
            template_xsl_rendering_views.TemplateXslRenderingDetail.as_view(),
            mock_user,
            param={"pk": str(ObjectId())},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(template_xsl_rendering_api, "get_by_id")
    @patch.object(template_xsl_rendering_api, "delete")
    def test_staff_returns_http_204(
        self,
        mock_template_xsl_rendering_api_get_by_id,
        mock_template_xsl_rendering_api_delete,
    ):
        mock_template_xsl_rendering_api_get_by_id.return_value = Mock()
        mock_template_xsl_rendering_api_delete.return_value = None
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_delete(
            template_xsl_rendering_views.TemplateXslRenderingDetail.as_view(),
            mock_user,
            param={"pk": str(ObjectId())},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
