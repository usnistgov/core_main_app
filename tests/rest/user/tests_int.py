""" Integration Test for User Rest API
"""
from rest_framework.status import HTTP_404_NOT_FOUND

from core_main_app.rest.user import views as user_rest_views
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    MongoIntegrationTransactionTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from tests.components.user.fixtures.fixtures import UserFixtures

user_fixture = UserFixtures()


class TestUserDetail(MongoIntegrationTransactionTestCase):
    def setUp(self):
        super(TestUserDetail, self).setUp()

    def test_get_returns_correct_user(self):
        # Arrange
        user = user_fixture.create_user()
        mock_user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            user_rest_views.UserRetrieveUpdateView.as_view(),
            mock_user,
            param={"pk": user.id},
        )

        # Assert
        self.assertEqual(user.id, response.data["id"])

    def test_get_returns_incorrect_user_raises_404(self):
        # Arrange
        user = user_fixture.create_user()
        mock_user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            user_rest_views.UserRetrieveUpdateView.as_view(),
            mock_user,
            param={"pk": user.id},
        )

        # Assert
        self.assertNotEqual(response.status_code, HTTP_404_NOT_FOUND)
