""" Integration Test for User
"""

from tests.components.user.fixtures.fixtures import UserFixtures
from django.contrib.auth.models import User
from core_main_app.components.user import api as user_api
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    IntegrationTransactionTestCase,
)


class TestUserGetActiveUsers(IntegrationTransactionTestCase):
    """Test User Get Active Users"""

    def test_get_active_users_returns_empty_list(self):
        """test get active users returns empty list

        Returns:

        """

        # Assert
        result = user_api.get_active_users()
        self.assertEqual(len(result), 0)

    def test_get_active_users_returns_list_users(self):
        """test get active users returns list users

        Returns:

        """
        UserFixtures().create_user(username="username")
        # Assert
        result = user_api.get_active_users()
        self.assertEqual(len(result), 1)
        self.assertTrue(user.is_active() for user in result)


class TestUserGetUserByUsername(IntegrationTransactionTestCase):
    """Test User Get User By Username"""

    def test_get_user_by_username_raises_error_when_does_not_exist(self):
        """test get user by username raises error when does not exist

        Returns:

        """

        # Assert
        with self.assertRaises(User.DoesNotExist):
            user_api.get_user_by_username("empty")

    def test_get_user_by_username_returns_user(self):
        """test get user by username returns user

        Returns:

        """
        user = UserFixtures().create_user(username="username")
        # Act
        result = user_api.get_user_by_username("username")
        # Assert
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, user.username)


class TestUserCreateAndSaveUser(IntegrationTransactionTestCase):
    """Test User Create And Save User"""

    def test_create_and_save_user_creates_user(self):
        """test create and save user creates user

        Returns:

        """

        # Act
        result = user_api.create_and_save_user(
            "username", "password", "firstname", "lastname", "email"
        )
        # Assert
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, "username")


class TestUserUpsert(IntegrationTransactionTestCase):
    """Test User Upsert"""

    def test_upsert_user_creates_user(self):
        """test upsert creates user

        Returns:

        """

        # Act
        result = user_api.upsert(User.objects.create_user(username="username"))
        # Assert
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, "username")

    def test_upsert_and_save_user_updates_user(self):
        """test upsert updates user

        Returns:

        """
        # Arrange
        user = user_api.create_and_save_user(
            "username", "password", "firstname", "lastname", "email"
        )
        user.username = "new_username"
        # Act
        result = user_api.upsert(user)
        # Assert
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, "new_username")


class TestUserGetAllUsersExceptList(IntegrationTransactionTestCase):
    """Test User Get All Users Except List"""

    def test_get_all_users_except_list_returns_empty_list(self):
        """test get all users except list returns empty list

        Returns:

        """
        # Arrange
        user = UserFixtures().create_user(username="username")
        # Act
        result = user_api.get_all_users_except_list([user])
        # Assert
        self.assertEqual(len(result), 0)

    def test_get_all_users_except_list_returns_list(self):
        """test get all users except list returns list

        Returns:

        """
        # Arrange
        user1 = UserFixtures().create_user(username="username1")
        user2 = UserFixtures().create_user(username="username2")
        user3 = UserFixtures().create_user(username="username3")

        # Act
        result = user_api.get_all_users_except_list([user1])
        # Assert
        self.assertEqual(len(result), 2)
        self.assertNotIn(user1, result)
        self.assertIn(user2, result)
        self.assertIn(user3, result)


class TestUserGetAllUsersExceptListId(IntegrationTransactionTestCase):
    """Test User Get All Users Except List Id"""

    def test_get_all_users_except_list_id_returns_empty_list(self):
        """test get all users except list id returns empty list

        Returns:

        """
        # Arrange
        user = UserFixtures().create_user(username="username")
        # Act
        result = user_api.get_all_users_except_list_id([user.id])
        # Assert
        self.assertEqual(len(result), 0)

    def test_get_all_users_except_list_id_returns_list(self):
        """test get all users except list id returns list

        Returns:

        """
        # Arrange
        user1 = UserFixtures().create_user(username="username1")
        user2 = UserFixtures().create_user(username="username2")
        user3 = UserFixtures().create_user(username="username3")

        # Act
        result = user_api.get_all_users_except_list_id([user1.id])
        # Assert
        self.assertEqual(len(result), 2)
        self.assertNotIn(user1, result)
        self.assertIn(user2, result)
        self.assertIn(user3, result)


class TestUserGetAllUsersByListId(IntegrationTransactionTestCase):
    """Test User Get All Users By List Id"""

    def test_get_all_users_by_list_id_returns_empty_list(self):
        """test get all users By list id returns empty list

        Returns:

        """
        # Act
        result = user_api.get_all_users_by_list_id([])
        # Assert
        self.assertEqual(len(result), 0)

    def test_get_all_users_by_list_id_returns_valid_user_id_only(self):
        """test get all users By list id returns valid user id only

        Returns:

        """
        # Arrange
        user = UserFixtures().create_user(username="username")
        # Act
        result = user_api.get_all_users_by_list_id([-1, user.id])
        # Assert
        self.assertEqual(len(result), 1)
        self.assertTrue(user in result)

    def test_get_all_users_by_list_id_returns_list(self):
        """test get all users by list id returns list

        Returns:

        """
        # Arrange
        user1 = UserFixtures().create_user(username="username1")
        user2 = UserFixtures().create_user(username="username2")
        user3 = UserFixtures().create_user(username="username3")

        # Act
        result = user_api.get_all_users_by_list_id([user1.id, user2.id])
        # Assert
        self.assertEqual(len(result), 2)
        self.assertIn(user1, result)
        self.assertIn(user2, result)
        self.assertNotIn(user3, result)


class TestUserGetIdUsernameDict(IntegrationTransactionTestCase):
    """Test User Get Id Username Dict"""

    def test_get_id_username_dict_returns_empty_list(self):
        """test get id username dict returns empty list

        Returns:

        """
        # Act
        result = user_api.get_id_username_dict([])
        # Assert
        self.assertEqual(len(result), 0)

    def test_get_id_username_dict_returns_list(self):
        """test get id username dict returns list

        Returns:

        """
        # Arrange
        user1 = UserFixtures().create_user(username="username1")
        user2 = UserFixtures().create_user(username="username2")
        UserFixtures().create_user(username="username3")

        # Act
        result = user_api.get_id_username_dict([user1, user2])
        # Assert
        self.assertEqual(len(result), 2)
