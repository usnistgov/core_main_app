""" Permission tests for `BlobProcessingModuleManageView` view from
`core_main_app.rest.blob_processing_module.views` package
"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from rest_framework import status

from core_main_app.rest.blob_processing_module import (
    views as blob_processing_module_views,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestPermissionsBlobProcessingModuleManageViewGet(TestCase):
    """Permission test for `BlobProcessingModuleManageView.get` method."""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""
        response = RequestMock.do_request_get(
            blob_processing_module_views.BlobProcessingModuleManageView.as_view(),
            None,
            param={"blob_processing_module_id": "mock_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_registered_returns_http_200(
        self,
        mock_blob_processing_module_serializer,  # noqa
        mock_blob_processing_module_api,
    ):
        """test_registered_returns_http_200"""
        mock_user = create_mock_user("1")
        mock_blob_processing_module_api.get_by_id.return_value = MagicMock()

        response = RequestMock.do_request_get(
            blob_processing_module_views.BlobProcessingModuleManageView.as_view(),
            mock_user,
            param={"blob_processing_module_id": "mock_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_staff_returns_http_200(
        self,
        mock_blob_processing_module_serializer,  # noqa
        mock_blob_processing_module_api,
    ):
        """test_staff_returns_http_200"""
        mock_user = create_mock_user("1", is_staff=True)
        mock_blob_processing_module_api.get_by_id.return_value = MagicMock()

        response = RequestMock.do_request_get(
            blob_processing_module_views.BlobProcessingModuleManageView.as_view(),
            mock_user,
            param={"blob_processing_module_id": "mock_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPermissionsBlobProcessingModuleManageViewPatch(TestCase):
    """Permission test for `BlobProcessingModuleManageView.patch` method."""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""
        response = RequestMock.do_request_patch(
            blob_processing_module_views.BlobProcessingModuleManageView.as_view(),
            None,
            param={"blob_processing_module_id": "mock_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_registered_returns_http_403(self):
        """test_registered_returns_http_403"""
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            blob_processing_module_views.BlobProcessingModuleManageView.as_view(),
            mock_user,
            param={"blob_processing_module_id": "mock_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views, "BlobProcessingModuleWriteSerializer"
    )
    def test_staff_returns_http_200(
        self,
        mock_blob_processing_module_serializer,  # noqa
        mock_blob_processing_module_api,
    ):
        """test_staff_returns_http_200"""
        mock_user = create_mock_user("1", is_staff=True)
        mock_blob_processing_module_api.get_by_id.return_value = MagicMock()

        response = RequestMock.do_request_patch(
            blob_processing_module_views.BlobProcessingModuleManageView.as_view(),
            mock_user,
            param={"blob_processing_module_id": "mock_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPermissionsBlobProcessingModuleManageViewDelete(TestCase):
    """Permission test for `BlobProcessingModuleManageView.delete` method."""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""
        response = RequestMock.do_request_delete(
            blob_processing_module_views.BlobProcessingModuleManageView.as_view(),
            None,
            param={"blob_processing_module_id": "mock_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_registered_returns_http_403(self):
        """test_registered_returns_http_403"""
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_delete(
            blob_processing_module_views.BlobProcessingModuleManageView.as_view(),
            mock_user,
            param={"blob_processing_module_id": "mock_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_staff_returns_http_204(self, mock_blob_processing_module_api):
        """test_staff_returns_http_201"""
        mock_user = create_mock_user("1", is_staff=True)
        mock_blob_processing_module_api.get_by_id.return_value = MagicMock()

        response = RequestMock.do_request_delete(
            blob_processing_module_views.BlobProcessingModuleManageView.as_view(),
            mock_user,
            param={"blob_processing_module_id": "mock_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
