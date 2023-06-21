""" Authentication tests for views
"""
from django.contrib.auth.models import AnonymousUser
from rest_framework import status

from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    IntegrationTransactionTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_main_app.views.user import views as user_views


class TestSetTimezone(IntegrationTransactionTestCase):
    """TestSetTimezone"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_get(
            user_views.set_timezone,
            self.anonymous,
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_authenticated_returns_http_200(self):
        """test_authenticated_returns_http_403

        Returns:

        """

        response = RequestMock.do_request_get(
            user_views.set_timezone,
            self.user1,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
