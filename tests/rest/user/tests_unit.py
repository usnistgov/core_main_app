"""Units tests for User rest api
"""
from django.test import SimpleTestCase
from mock.mock import patch

from core_main_app.rest.user import views as user_rest_views
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_main_app.components.user import api as user_api


class TestGetAllUserList(SimpleTestCase):
    def setUp(self):
        super(TestGetAllUserList, self).setUp()
        self.data = None

    @patch.object(user_api, "get_all_users")
    def test_get_all_returns_list(self, get_all_users):
        # Arrange
        user = create_mock_user("0", is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            user_rest_views.UserList.as_view(), user, self.data
        )

        # Assert
        excepted_result = []
        self.assertEqual(response.data, excepted_result)
