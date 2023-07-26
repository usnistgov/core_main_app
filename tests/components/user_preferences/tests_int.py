""" Integration Test for User Preferences
"""
from django.core.exceptions import ValidationError
from tests.components.user_preferences.fixtures.fixtures import (
    UserPreferencesFixtures,
)

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

    def test_upsert_user_preferences_creates_preferences(self):
        """test_upsert_user_preferences_creates_preferences

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

    def test_upsert_user_preferences_updates_preferences(self):
        """test_upsert_user_preferences_updates_preferences

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

    def test_upsert_user_preferences_raises_error_when_user_had_already_preferences(
        self,
    ):
        """test_upsert_user_preferences_raises_error_when_user_had_already_preferences

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        user_preferences = UserPreferences(user_id="1", timezone="GMT")

        # Act  # Assert
        with self.assertRaises(ValidationError):
            user_preferences_api.upsert(user_preferences, user)


class TestUserPreferencesDelete(IntegrationTransactionTestCase):
    """Test User Preferences Delete"""

    fixture = fixture_user_preferences

    def test_delete_user_preferences_delete_preferences(self):
        """test_delete_user_preferences_delete_preferences

        Args:

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        user_preferences_api.delete(self.fixture.user_preferences_1, user)

        self.assertEquals(self.fixture.user_preferences_1.id, None)


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

    def test_get_user_preferences_by_user_raises_dne_exception_when_no_preferences_founded(
        self,
    ):
        """test_get_user_preferences_by_user_raises_dne_exception_when_no_preferences_founded

        Args:

        Returns:

        """

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            user_preferences_api.get_by_user(create_mock_user("0"))
