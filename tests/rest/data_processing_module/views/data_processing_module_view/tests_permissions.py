""" Permission tests for `DataProcessingModuleView` view from
`core_main_app.rest.data_processing_module.views` package
"""

from unittest.mock import patch

from django.test import SimpleTestCase
from rest_framework import status

from core_main_app.rest.data import views as data_rest_views
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestDataRunProcessingModulePost(SimpleTestCase):
    """Permission tests for `DataRunProcessingModule.post` method."""

    def setUp(self):
        """setUp"""
        self.mock_data = {"data_id": 1, "processing_module_id": 1}

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""
        response = RequestMock.do_request_post(
            data_rest_views.DataRunProcessingModule.as_view(),
            None,
            param=self.mock_data,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(data_rest_views, "check_can_write")
    @patch.object(data_rest_views, "data_api")
    @patch.object(data_rest_views, "data_processing_module_tasks")
    def test_registered_returns_http_200(
        self,
        mock_data_processing_module_tasks,
        mock_data_api,
        mock_check_can_write,
    ):
        """test_registered_returns_http_200"""
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            data_rest_views.DataRunProcessingModule.as_view(),
            mock_user,
            param=self.mock_data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_rest_views, "check_can_write")
    @patch.object(data_rest_views, "data_api")
    @patch.object(data_rest_views, "data_processing_module_tasks")
    def test_staff_returns_200(
        self,
        mock_data_processing_module_tasks,
        mock_data_api,
        mock_check_can_write,
    ):
        """test_staff_returns_200"""
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            data_rest_views.DataRunProcessingModule.as_view(),
            mock_user,
            param=self.mock_data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
