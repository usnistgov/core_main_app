""" Test units for User Preferences
"""

from unittest.case import TestCase
from unittest.mock import patch

from django.core.exceptions import ValidationError, ObjectDoesNotExist

from core_main_app.commons import exceptions
from core_main_app.components.user_preferences import (
    api as user_preferences_api,
)
from core_main_app.components.user_preferences.admin_site import (
    CustomUserPreferencesAdmin,
)
from core_main_app.components.user_preferences.models import UserPreferences
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestUserPreferencesUpsert(TestCase):
    """Test User Preferences Upsert"""

    @patch.object(UserPreferences, "save")
    def test_user_preferences_upsert_returns_object(self, mock_save):
        """test_user_preferences_upsert_return_object

        Args:
            mock_save:

        Returns:

        """
        # Arrange
        mock_user_preferences = UserPreferences(
            user_id="1", timezone="Europe/Paris"
        )

        mock_save.return_value = mock_user_preferences

        # Act
        result = user_preferences_api.upsert(
            mock_user_preferences, create_mock_user("1")
        )

        # Assert
        self.assertIsInstance(result, UserPreferences)

    @patch.object(UserPreferences, "save")
    def test_user_preferences_upsert_raise_validation_error_when_invalid_timezone_set(
        self, mock_save
    ):
        """test_user_preferences_upsert_raise_validation_error_when_invalid_timezone_set

        Args:
            mock_save:

        Returns:

        """
        # Arrange
        mock_user_preferences = UserPreferences(
            user_id="1", timezone="bad timezone"
        )

        mock_save.side_effect = exceptions.ModelError("")

        # Act + Assert
        with self.assertRaises(ValidationError):
            user_preferences_api.upsert(
                mock_user_preferences, create_mock_user("1")
            )

    @patch.object(UserPreferences, "save")
    def test_user_preferences_upsert_raise_error_when_user_has_already_user_preferences(
        self, mock_save
    ):
        """test_user_preferences_upsert_raise_error_when_user_has_already_user_preferences

        Args:
            mock_save:

        Returns:

        """
        # Arrange
        mock_user_preferences = UserPreferences(
            user_id="1", timezone="Europe/Paris"
        )

        mock_save.side_effect = exceptions.ModelError("")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            user_preferences_api.upsert(
                mock_user_preferences, create_mock_user("1")
            )


class TestUserPreferencesDelete(TestCase):
    """Test User Preferences Delete"""

    @patch.object(UserPreferences, "delete")
    def test_delete_user_preferences_deletes(self, mock_delete):
        """test_delete_user_preferences_deletes

        Args:
            mock_delete:

        Returns:

        """
        # Arrange
        mock_user_preferences = UserPreferences(user_id="1", timezone="test")

        mock_delete.return_value = []

        # Act
        user_preferences_api.delete(
            mock_user_preferences, create_mock_user("1")
        )

    @patch.object(UserPreferences, "delete")
    def test_delete_user_preferences_raises_dne_exception(self, mock_delete):
        """test_delete_user_preferences_raises_dne_exception

        Args:
            mock_delete:
        Returns:

        """
        # Arrange
        mock_user_preferences = UserPreferences(user_id="1", timezone="test")
        mock_delete.side_effect = exceptions.DoesNotExist("")
        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            user_preferences_api.delete(
                mock_user_preferences, create_mock_user("1")
            )


class TestUserPreferencesGetByUser(TestCase):
    """Test User Preferences Get By User"""

    @patch.object(UserPreferences, "objects")
    def test_get_user_preferences_by_user_returns_object(self, mock_objects):
        """test_get_user_preferences_by_user_return_object

        Args:
            mock_objects:

        Returns:

        """
        # Arrange
        mock_user_preferences = UserPreferences(user_id="1", timezone="test")

        mock_objects.get.return_value = mock_user_preferences

        # Act
        result = user_preferences_api.get_by_user(
            create_mock_user("1", is_superuser=True)
        )

        # Assert
        self.assertEquals(result.timezone, "test")
        self.assertEquals(result.user_id, "1")

    @patch.object(UserPreferences, "objects")
    def test_get_user_preferences_by_user_raises_dne_exception(
        self, mock_objects
    ):
        """test_get_user_preferences_by_user_raises_dne_exception

        Args:
            mock_objects

        Returns:

        """
        # Arrange
        mock_objects.get.side_effect = ObjectDoesNotExist("")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            user_preferences_api.get_by_user(
                create_mock_user("1", is_superuser=True)
            )

    @patch.object(UserPreferences, "objects")
    def test_get_user_preferences_by_user_raises_model_error_exception(
        self, mock_objects
    ):
        """test_get_user_preferences_by_user_raises_model_error_exception

        Args:

        Returns:

        """
        # Arrange
        mock_objects.get.side_effect = exceptions.ModelError("")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            user_preferences_api.get_by_user(
                create_mock_user("1", is_superuser=True)
            )


class TestCustomUserPreferencesAdmin(TestCase):
    """Test Custom User Preferences Admin"""

    def test_custom_user_preferences_admin(self):
        """test_custom_user_preferences_admin

        Args:

        Returns:

        """
        # Arrange
        custom_admin_site = CustomUserPreferencesAdmin(UserPreferences, None)

        # Assert
        self.assertTrue("user_id" in custom_admin_site.list_display)
        self.assertTrue("timezone" in custom_admin_site.list_display)

    def test_custom_user_preferences_admin_add_permission(self):
        """test_custom_user_preferences_admin_add_permission

        Args:

        Returns:

        """
        # Arrange
        custom_admin_site = CustomUserPreferencesAdmin(UserPreferences, None)

        # Assert
        self.assertFalse(custom_admin_site.has_add_permission(request=None))
