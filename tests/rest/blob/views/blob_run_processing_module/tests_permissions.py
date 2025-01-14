""" Permission tests tests for `BlobRunProcessingModule` views in
`core_main_app.rest.blob.views` package.
"""

from unittest import TestCase
from unittest.mock import patch

from rest_framework import status

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock

from core_main_app.rest.blob import views as blob_views


class TestBlobRunProcessingModulePost(TestCase):
    """Permission tests for `BlobRunProcessingModule.post` method."""

    def setUp(self):
        """setUp"""
        self.mock_data = {"blob_id": 1, "processing_module_id": 1}

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""
        response = RequestMock.do_request_post(
            blob_views.BlobRunProcessingModule.as_view(),
            None,
            param=self.mock_data,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(blob_views, "blob_processing_module_tasks")
    def test_registered_returns_http_200(
        self, mock_blob_processing_module_tasks
    ):
        """test_registered_returns_http_200"""
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            blob_views.BlobRunProcessingModule.as_view(),
            mock_user,
            param=self.mock_data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(blob_views, "blob_processing_module_tasks")
    def test_staff_returns_200(self, mock_blob_processing_module_tasks):
        """test_staff_returns_200"""
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            blob_views.BlobRunProcessingModule.as_view(),
            mock_user,
            param=self.mock_data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
