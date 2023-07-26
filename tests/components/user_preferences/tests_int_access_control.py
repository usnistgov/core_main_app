""" Access Control Test for User Preferences
"""
from unittest.mock import patch, Mock

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from tests.components.user_preferences.fixtures.fixtures import (
    UserPreferencesFixtures,
)

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
from core_main_app.components.user_preferences import (
    api as user_preferences_api,
)
from core_main_app.components.user_preferences.models import UserPreferences
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    IntegrationTransactionTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user

fixture_user_preferences = UserPreferencesFixtures()


class TestUserPreferencesUpsert(IntegrationTransactionTestCase):
    """Test User Preferences Upsert"""

    fixture = fixture_user_preferences

    def test_upsert_user_preferences_as_owner_creates_preferences(self):
        """test_upsert_user_preferences_as_owner_creates_preferences

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("4")

        user_preferences = UserPreferences(user_id="4", timezone="GMT")
        # Act
        result = user_preferences_api.upsert(user_preferences, user)

        # Assert
        self.assertEquals(result.timezone, user_preferences.timezone)
        self.assertEquals(result.user_id, user.id)

    def test_upsert_user_preferences_as_superuser_creates_preferences(self):
        """test_upsert_user_preferences_as_superuser_creates_preferences

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        user_preferences = UserPreferences(user_id="4", timezone="GMT")
        # Act
        result = user_preferences_api.upsert(user_preferences, user)

        # Assert
        self.assertEquals(result.timezone, user_preferences.timezone)
        self.assertEquals(result.user_id, user_preferences.user_id)

    def test_upsert_user_preferences_as_user_raises_access_control(self):
        """test_upsert_user_preferences_as_user_raises_access_control

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        user_preferences = UserPreferences(user_id="4", timezone="GMT")
        # Act
        with self.assertRaises(AccessControlError):
            user_preferences_api.upsert(user_preferences, user)

    def test_upsert_user_preferences_as_anonymous_raises_access_control(self):
        """test_upsert_user_preferences_as_anonymous_raises_access_control

        Args:

        Returns:

        """
        # Arrange
        user = AnonymousUser()

        user_preferences = UserPreferences(user_id="4", timezone="GMT")
        # Act
        with self.assertRaises(AccessControlError):
            user_preferences_api.upsert(user_preferences, user)

    def test_upsert_user_preferences_as_owner_updates_preferences(self):
        """test_upsert_user_preferences_as_owner_updates_preferences

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        user_preferences = self.fixture.user_preferences_1
        user_preferences.timezone = "Europe/Paris"
        # Act
        result = user_preferences_api.upsert(user_preferences, user)

        # Assert
        self.assertEquals(result.timezone, "Europe/Paris")
        self.assertEquals(result.user_id, user.id)

    def test_upsert_others_user_preferences_as_superuser_updates_preferences(
        self,
    ):
        """test_upsert_others_user_preferences_as_superuser_updates_preferences

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        user_preferences = self.fixture.user_preferences_3
        user_preferences.timezone = "Europe/Paris"
        # Act
        result = user_preferences_api.upsert(user_preferences, user)

        # Assert
        self.assertEquals(result.timezone, "Europe/Paris")
        self.assertEquals(result.user_id, user_preferences.user_id)

    def test_upsert_others_user_preferences_as_user_raises_access_control(
        self,
    ):
        """test_upsert_others_user_preferences_as_user_raises_access_control

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        user_preferences = self.fixture.user_preferences_2
        user_preferences.timezone = "fake_zone"

        # Act
        with self.assertRaises(AccessControlError):
            user_preferences_api.upsert(user_preferences, user)

    def test_upsert_others_user_preferences_as_anonymous_raises_access_control(
        self,
    ):
        """test_upsert_others_user_preferences_as_anonymous_raises_access_control

        Args:

        Returns:

        """
        # Arrange
        user = AnonymousUser()

        user_preferences = self.fixture.user_preferences_2
        user_preferences.timezone = "fake_zone"

        # Act
        with self.assertRaises(AccessControlError):
            user_preferences_api.upsert(user_preferences, user)

    def test_upsert_user_preferences_as_owner_raises_error_when_user_had_already_preferences(
        self,
    ):
        """test_upsert_user_preferences_as_owner_raises_error_when_user_had_already_preferences

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        user_preferences = UserPreferences(user_id="1", timezone="GMT")

        # Act  # Assert
        with self.assertRaises(ValidationError):
            user_preferences_api.upsert(user_preferences, user)

    def test_upsert_others_user_preferences_as_superuser_raises_error_when_user_had_already_preferences(
        self,
    ):
        """test_upsert_others_user_preferences_as_superuser_raises_error_when_user_had_already_preferences

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("0", is_superuser=True)

        user_preferences = UserPreferences(user_id="1", timezone="GMT")

        # Act  # Assert
        with self.assertRaises(ValidationError):
            user_preferences_api.upsert(user_preferences, user)


class TestUserPreferencesDelete(IntegrationTransactionTestCase):
    """Test User Preferences Delete"""

    fixture = fixture_user_preferences

    def test_delete_user_preferences_as_owner_delete_preferences(self):
        """test_delete_user_preferences_as_owner_delete_preferences

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        user_preferences_api.delete(self.fixture.user_preferences_1, user)

        self.assertEquals(self.fixture.user_preferences_1.id, None)

    def test_delete_user_preferences_as_superuser_delete_preferences(self):
        """test_delete_user_preferences_as_superuser_delete_preferences

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        user_preferences_api.delete(self.fixture.user_preferences_1, user)

        self.assertEquals(self.fixture.user_preferences_1.id, None)

    def test_delete_others_user_preferences_as_superuser_delete_preferences(
        self,
    ):
        """test_delete_others_user_preferences_as_superuser_delete_preferences

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        # Act
        user_preferences_api.delete(self.fixture.user_preferences_3, user)

        self.assertEquals(self.fixture.user_preferences_3.id, None)

    def test_delete_others_user_preferences_as_user_raises_access_control(
        self,
    ):
        """test_delete_others_user_preferences_as_user_raises_access_control

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        user_preferences = self.fixture.user_preferences_2
        user_preferences.timezone = "fake_zone"

        # Act
        with self.assertRaises(AccessControlError):
            user_preferences_api.delete(user_preferences, user)

    def test_update_others_user_preferences_as_anonymous_raises_access_control(
        self,
    ):
        """test_update_others_user_preferences_as_anonymous_raises_access_control

        Args:

        Returns:

        """
        # Arrange
        user = AnonymousUser()

        user_preferences = self.fixture.user_preferences_2
        user_preferences.timezone = "fake_zone"

        # Act
        with self.assertRaises(AccessControlError):
            user_preferences_api.delete(user_preferences, user)


class TestUserPreferencesGetByUser(IntegrationTransactionTestCase):
    """Test User Preferences Get By User"""

    fixture = fixture_user_preferences

    def test_get_user_preferences_by_user_as_owner_returns_preferences(self):
        """test_get_user_preferences_by_user_as_owner_returns_preferences

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        result = user_preferences_api.get_by_user(user)

        # Assert
        self.assertEquals(result.timezone, "UTC")
        self.assertEquals(result.user_id, user.id)

    @patch(
        "core_main_app.components.user_preferences.models.UserPreferences.get_by_user"
    )
    def test_get_user_preferences_with_wrong_owner_raises_acl_error(
        self, mock_get_by_user
    ):
        """test_get_user_preferences_with_wrong_owner_raises_acl_error

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        mock_user_preferences = Mock(UserPreferences)
        mock_user_preferences.user_id = "2"
        mock_get_by_user.return_value = mock_user_preferences

        # Act + Assert
        with self.assertRaises(AccessControlError):
            user_preferences_api.get_by_user(user)

    def test_get_others_user_preferences_with_no_user_raises_access_control_error(
        self,
    ):
        """test_get_others_user_preferences_by_user_as_user_raises_access_control_error

        Args:

        Returns:

        """
        # Act  # Assert
        with self.assertRaises(AccessControlError):
            user_preferences_api.get_by_user(None)

    def test_get_others_user_preferences_by_user_as_anonymous_raises_access_control_error(
        self,
    ):
        """test_get_others_user_preferences_by_user_as_anonymous_raises_access_control_error

        Args:

        Returns:

        """
        # Arrange
        user = AnonymousUser()

        # Act  # Assert
        with self.assertRaises(AccessControlError):
            user_preferences_api.get_by_user(user)

    def test_get_user_preferences_by_user_as_user_raises_dne_exception_when_no_preferences_founded(
        self,
    ):
        """test_get_user_preferences_by_user_as_user_raises_dne_exception_when_no_preferences_founded

        Args:

        Returns:

        """

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            user_preferences_api.get_by_user(create_mock_user("0"))

    def test_get_user_preferences_by_user_as_superuser_raises_dne_exception_when_no_preferences_found(
        self,
    ):
        """test_get_user_preferences_by_user_as_superuser_raises_dne_exception_when_no_preferences_found

        Args:

        Returns:

        """

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            user_preferences_api.get_by_user(
                create_mock_user("0", is_superuser=True)
            )
