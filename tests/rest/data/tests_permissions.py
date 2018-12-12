""" Authentication tests for Data REST API
"""
from django.test import SimpleTestCase
from mock.mock import patch
from rest_framework import status

from core_main_app.components.data.models import Data
from core_main_app.rest.data.serializers import DataSerializer
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_main_app.rest.data import views as data_rest_views
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestDataListPostPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_post(
            data_rest_views.DataList.as_view(),
            None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(DataSerializer, "is_valid")
    @patch.object(DataSerializer, "save")
    @patch.object(DataSerializer, "data")
    def test_authenticated_returns_http_201(self, data_serializer_data, data_serializer_save, data_serializer_valid):
        data_serializer_valid.return_value = True
        data_serializer_save.return_value = None
        data_serializer_data.return_value = {}

        mock_user = create_mock_user('1')

        response = RequestMock.do_request_post(
            data_rest_views.DataList.as_view(),
            mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(DataSerializer, "is_valid")
    @patch.object(DataSerializer, "save")
    @patch.object(DataSerializer, "data")
    def test_staff_returns_http_201(self, data_serializer_data, data_serializer_save, data_serializer_valid):
        data_serializer_valid.return_value = True
        data_serializer_save.return_value = None
        data_serializer_data.return_value = {}

        mock_user = create_mock_user('1', is_staff=True)

        response = RequestMock.do_request_post(
            data_rest_views.DataList.as_view(),
            mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestDataListGetPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):

        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(),
            None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(Data, "get_all_by_user_id")
    def test_authenticated_returns_http_200(self, data_get_all_by_user):
        data_get_all_by_user.return_value = {}

        mock_user = create_mock_user('1')

        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(),
            mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Data, "get_all_by_user_id")
    def test_staff_returns_http_200(self, data_get_all_by_user):
        data_get_all_by_user.return_value = {}

        mock_user = create_mock_user('1', is_staff=True)

        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(),
            mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
