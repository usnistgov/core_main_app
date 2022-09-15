"""Units tests for User rest api
"""
from django.test import TestCase

from core_main_app.rest.user import views as user_rest_views
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestGetAllUserList(TestCase):
    """TestGetAllUserList"""

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()
        self.data = None

    def test_get_all_returns_list(self):
        """test_get_all_returns_list

        Returns:

        """
        # Arrange
        user = create_mock_user("0", is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            user_rest_views.UserListCreateView.as_view(), user, self.data
        )

        # Assert
        excepted_result = []
        self.assertEqual(response.data, excepted_result)
