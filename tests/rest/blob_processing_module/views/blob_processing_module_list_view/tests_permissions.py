""" Permission tests for `BlobProcessingModuleListView` view from
`core_main_app.rest.blob_processing_module.views` package
"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from rest_framework import status

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock

from core_main_app.rest.blob_processing_module import (
    views as blob_processing_module_views,
)


class TestPermissionsBlobProcessingModuleListViewGet(TestCase):
    """Permission test for `BlobProcessingModuleListView.get` method."""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""
        response = RequestMock.do_request_get(
            blob_processing_module_views.BlobProcessingModuleListView.as_view(),
            None,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views, "BlobProcessingModuleWriteSerializer"
    )
    def test_registered_returns_http_200(
        self,
        mock_blob_processing_module_serializer,  # noqa
        mock_blob_processing_module_api,  # noqa
    ):
        """test_registered_returns_http_200"""
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            blob_processing_module_views.BlobProcessingModuleListView.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views, "BlobProcessingModuleWriteSerializer"
    )
    def test_staff_returns_http_200(
        self,
        mock_blob_processing_module_serializer,  # noqa
        mock_blob_processing_module_api,  # noqa
    ):
        """test_staff_returns_http_200"""
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            blob_processing_module_views.BlobProcessingModuleListView.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPermissionsBlobProcessingModuleListViewPost(TestCase):
    """Permission test for `BlobProcessingModuleListView.post` method."""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""
        response = RequestMock.do_request_post(
            blob_processing_module_views.BlobProcessingModuleListView.as_view(),
            None,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_registered_returns_http_403(self):
        """test_registered_returns_http_403"""
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            blob_processing_module_views.BlobProcessingModuleListView.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_staff_returns_http_201(
        self,
        mock_get_serializer,
    ):
        """test_staff_returns_http_201"""
        mock_user = create_mock_user("1", is_staff=True)

        mock_get_serializer.return_value = MagicMock()

        response = RequestMock.do_request_post(
            blob_processing_module_views.BlobProcessingModuleListView.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
