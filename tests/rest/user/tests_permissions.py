""" Authentication tests for User REST API
"""
from django.test import TestCase
from rest_framework import status
from tests.components.user.fixtures.fixtures import UserFixtures

from core_main_app.rest.user import views as user_rest_views
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    MongoIntegrationTransactionTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock

user_fixture = UserFixtures()


class TestUserGetPermissions(MongoIntegrationTransactionTestCase):
    """TestUserGetPermissions"""

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_get(
            user_rest_views.UserRetrieveUpdateView.as_view(), None, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Returns:

        """
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            user_rest_views.UserRetrieveUpdateView.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_returns_http_200(self):
        """test_staff_returns_http_200

        Returns:

        """
        mock_get_user = user_fixture.create_user("mock_user")

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            user_rest_views.UserRetrieveUpdateView.as_view(),
            mock_user,
            param={"pk": mock_get_user.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserListGetPermissions(TestCase):
    """TestUserListGetPermissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_get(
            user_rest_views.UserListCreateView.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Returns:

        """
        mock_user = create_mock_user("1")
        response = RequestMock.do_request_get(
            user_rest_views.UserListCreateView.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_returns_http_200(self):
        """test_staff_returns_http_200

        Returns:

        """
        mock_user = create_mock_user("1", is_staff=True)
        response = RequestMock.do_request_get(
            user_rest_views.UserListCreateView.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
