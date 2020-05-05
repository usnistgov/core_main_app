""" Authentication tests for User REST API
"""
from django.test import SimpleTestCase

from mock.mock import patch
from rest_framework import status

from core_main_app.rest.user import views as user_rest_views
from core_main_app.components.user import api as user_api
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestUserGetPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(
            user_rest_views.UserDetail.as_view(), None, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            user_rest_views.UserDetail.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(user_api, "get_user_by_id")
    def test_staff_returns_http_200(self, user_get_by_id):
        mock_get_user = create_mock_user("0")
        user_get_by_id.return_value = mock_get_user

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            user_rest_views.UserDetail.as_view(),
            mock_user,
            param={"pk": mock_get_user.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserListGetPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(user_rest_views.UserList.as_view(), None)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        mock_user = create_mock_user("1")
        response = RequestMock.do_request_get(
            user_rest_views.UserList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(user_api, "get_all_users")
    def test_staff_returns_http_200(self, get_all_users):
        get_all_users.return_value = {}
        mock_user = create_mock_user("1", is_staff=True)
        response = RequestMock.do_request_get(
            user_rest_views.UserList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
