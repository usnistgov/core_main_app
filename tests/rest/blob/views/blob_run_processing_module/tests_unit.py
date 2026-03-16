"""Unit tests for `BlobRunProcessingModule` views in `core_main_app.rest.blob.views`
package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from rest_framework import status
from rest_framework.status import HTTP_403_FORBIDDEN

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.blob_processing_module.models import (
    BlobProcessingModule,
)
from core_main_app.rest.blob import views as blob_views


class TestBlobRunProcessingModulePost(TestCase):
    """Unit tests for `BlobRunProcessingModule.post` method."""

    def setUp(self):
        """setUp"""
        self.mock_view = blob_views.BlobRunProcessingModule()
        self.kwargs = {
            "request": MagicMock(),
            "blob_id": MagicMock(),
            "processing_module_id": MagicMock(),
        }

    def test_no_processing_module_id_returns_400(self):
        """test_no_processing_module_id_returns_400"""
        self.kwargs["processing_module_id"] = None

        result = self.mock_view.post(**self.kwargs)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_blob_id_returns_400(self):
        """test_no_blob_id_returns_400"""
        self.kwargs["blob_id"] = None

        result = self.mock_view.post(**self.kwargs)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(blob_views, "check_can_write")
    @patch.object(blob_views, "blob_api")
    @patch.object(blob_views, "blob_processing_module_tasks")
    def test_process_blob_blob_api_called(
        self,
        mock_blob_processing_module_tasks,
        mock_blob_api,
        mock_check_can_write,
    ):
        """test_process_blob_blob_api_called"""
        self.mock_view.post(**self.kwargs)
        self.assertTrue(mock_blob_api.get_by_id.called)

    @patch.object(blob_views, "check_can_write")
    @patch.object(blob_views, "blob_api")
    @patch.object(blob_views, "blob_processing_module_tasks")
    def test_process_blob_return_http_403_when_acl_error_in_blob_api(
        self,
        mock_blob_processing_module_tasks,
        mock_blob_api,
        mock_check_can_write,
    ):
        """test_process_blob_blob_api_called"""
        mock_blob_api.get_by_id.side_effect = AccessControlError("error")
        response = self.mock_view.post(**self.kwargs)

        self.assertTrue(mock_blob_api.get_by_id.called)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    @patch.object(blob_views, "check_can_write")
    @patch.object(blob_views, "blob_api")
    @patch.object(blob_views, "blob_processing_module_tasks")
    def test_process_blob_called(
        self,
        mock_blob_processing_module_tasks,
        mock_blob_api,
        mock_check_can_write,
    ):
        """test_process_blob_called"""
        self.mock_view.post(**self.kwargs)

        mock_blob_processing_module_tasks.process_blob_with_module.apply_async.assert_called_with(
            (
                self.kwargs["processing_module_id"],
                self.kwargs["blob_id"],
                BlobProcessingModule.RUN_ON_DEMAND,
                self.kwargs["request"].user.id,
            )
        )

    @patch.object(blob_views, "check_can_write")
    @patch.object(blob_views, "blob_api")
    @patch.object(blob_views, "blob_processing_module_tasks")
    def test_process_blob_exception_returns_500(
        self,
        mock_blob_processing_module_tasks,
        mock_blob_api,
        mock_check_can_write,
    ):
        """test_process_blob_exception_returns_500"""
        mock_blob_processing_module_tasks.process_blob_with_module.apply_async.side_effect = Exception(
            "mock_process_blob_exception"
        )

        result = self.mock_view.post(**self.kwargs)
        self.assertEqual(
            result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(blob_views, "check_can_write")
    @patch.object(blob_views, "blob_api")
    @patch.object(blob_views, "blob_processing_module_tasks")
    def test_success_returns_200(
        self,
        mock_blob_processing_module_tasks,
        mock_blob_api,
        mock_check_can_write,
    ):
        """test_success_returns_200"""
        result = self.mock_view.post(**self.kwargs)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
