"""Unit tests for `DataRunProcessingModuleView` view from
`core_main_app.rest.data_processing_module.views` package
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from rest_framework import status
from rest_framework.status import HTTP_403_FORBIDDEN

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.data_processing_module.models import (
    DataProcessingModule,
)
from core_main_app.rest.data import views as data_rest_views


class TestDataRunProcessingModulePost(TestCase):
    """Unit tests for `DataRunProcessingModule.post` method."""

    def setUp(self):
        """setUp"""
        self.mock_view = data_rest_views.DataRunProcessingModule()
        self.kwargs = {
            "request": MagicMock(),
            "data_id": MagicMock(),
            "processing_module_id": MagicMock(),
        }

    def test_no_processing_module_id_returns_400(self):
        """test_no_processing_module_id_returns_400"""
        self.kwargs["processing_module_id"] = None

        result = self.mock_view.post(**self.kwargs)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_data_id_returns_400(self):
        """test_no_data_id_returns_400"""
        self.kwargs["data_id"] = None

        result = self.mock_view.post(**self.kwargs)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(data_rest_views, "check_can_write")
    @patch.object(data_rest_views, "data_api")
    @patch.object(data_rest_views, "data_processing_module_tasks")
    def test_process_data_data_api_called(
        self,
        mock_data_processing_module_tasks,
        mock_data_api,
        mock_check_can_write,
    ):
        """test_process_data_data_api_called"""
        self.mock_view.post(**self.kwargs)
        self.assertTrue(mock_data_api.get_by_id.called)

    @patch.object(data_rest_views, "check_can_write")
    @patch.object(data_rest_views, "data_api")
    @patch.object(data_rest_views, "data_processing_module_tasks")
    def test_process_data_return_http_403_when_acl_error_in_data_api(
        self,
        mock_data_processing_module_tasks,
        mock_data_api,
        mock_check_can_write,
    ):
        """test_process_data_data_api_called"""
        mock_data_api.get_by_id.side_effect = AccessControlError("error")
        response = self.mock_view.post(**self.kwargs)

        self.assertTrue(mock_data_api.get_by_id.called)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    @patch.object(data_rest_views, "check_can_write")
    @patch.object(data_rest_views, "data_api")
    @patch.object(data_rest_views, "data_processing_module_tasks")
    def test_process_data_called(
        self,
        mock_data_processing_module_tasks,
        mock_data_api,
        mock_check_can_write,
    ):
        """test_process_data_called"""
        self.mock_view.post(**self.kwargs)

        mock_data_processing_module_tasks.process_data_with_module.apply_async.assert_called_with(
            (
                self.kwargs["processing_module_id"],
                self.kwargs["data_id"],
                DataProcessingModule.RUN_ON_DEMAND,
                self.kwargs["request"].user.id,
            )
        )

    @patch.object(data_rest_views, "check_can_write")
    @patch.object(data_rest_views, "data_api")
    @patch.object(data_rest_views, "data_processing_module_tasks")
    def test_process_data_exception_returns_500(
        self,
        mock_data_processing_module_tasks,
        mock_data_api,
        mock_check_can_write,
    ):
        """test_process_data_exception_returns_500"""
        mock_data_processing_module_tasks.process_data_with_module.apply_async.side_effect = Exception(
            "mock_process_data_exception"
        )

        result = self.mock_view.post(**self.kwargs)
        self.assertEqual(
            result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(data_rest_views, "check_can_write")
    @patch.object(data_rest_views, "data_api")
    @patch.object(data_rest_views, "data_processing_module_tasks")
    def test_success_returns_200(
        self,
        mock_data_processing_module_tasks,
        mock_data_api,
        mock_check_can_write,
    ):
        """test_success_returns_200"""
        result = self.mock_view.post(**self.kwargs)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
