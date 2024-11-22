""" Permission tests for `BlobProcessingModuleView` view from
`core_main_app.rest.blob_processing_module.views` package
"""

from unittest import TestCase

from rest_framework import status

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock

from core_main_app.rest.blob_processing_module import (
    views as blob_processing_module_views,
)


class TestPermissionsBlobProcessingModuleViewGet(TestCase):
    """Permission test for `BlobProcessingModuleView.get` method."""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""
        response = RequestMock.do_request_get(
            blob_processing_module_views.BlobProcessingModuleView.as_view(),
            None,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_registered_returns_http_200(self):
        """test_registered_returns_http_200"""
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            blob_processing_module_views.BlobProcessingModuleView.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_returns_http_200(self):
        """test_staff_returns_http_200"""
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            blob_processing_module_views.BlobProcessingModuleView.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
