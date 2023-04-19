""" Integration Test for User Fixtures
"""

from tests.components.user.fixtures.fixtures import UserFixtures

from core_main_app.components.user import api as user_api
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    IntegrationTransactionTestCase,
)


class TestUserFixtures(IntegrationTransactionTestCase):
    """Test User fixtures"""

    def test_create_user(self):
        """test create user

        Returns:

        """
        # Context
        user_count = len(user_api.get_all_users())
        self.assertEqual(user_count, 0)

        # Act
        UserFixtures().create_user(username="test username")

        # Assert
        list_user = user_api.get_all_users()
        self.assertEqual(list_user[0].username, "test username")
        self.assertEqual(len(list_user), user_count + 1)
        self.assertFalse(list_user[0].is_superuser)

    def test_create_super_user(self):
        """test create super user

        Returns:

        """
        # Context
        user_count = len(user_api.get_all_users())
        self.assertEqual(user_count, 0)

        # Act
        UserFixtures().create_super_user(username="test username")

        # Assert
        list_user = user_api.get_all_users()
        self.assertEqual(list_user[0].username, "test username")
        self.assertEqual(len(list_user), user_count + 1)
        self.assertTrue(list_user[0].is_superuser)
