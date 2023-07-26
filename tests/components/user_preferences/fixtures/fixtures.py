""" Fixtures files for User Preferences
"""

from core_main_app.components.user_preferences.models import UserPreferences

from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)


class UserPreferencesFixtures(FixtureInterface):
    """User Preferences Fixture"""

    user_preferences_1 = None
    user_preferences_2 = None
    user_preferences_3 = None
    users_preferences_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_users_preferences_collection()

    def generate_users_preferences_collection(self):
        """Generate a Data collection.

        Returns:

        """
        self.user_preferences_1 = UserPreferences(user_id="1", timezone="UTC")
        self.user_preferences_1.save()
        self.user_preferences_2 = UserPreferences(
            user_id="2", timezone="US/Central"
        )
        self.user_preferences_2.save()
        self.user_preferences_3 = UserPreferences(user_id="3", timezone="UTC")
        self.user_preferences_3.save()

        self.users_preferences_collection = [
            self.user_preferences_1,
            self.user_preferences_2,
            self.user_preferences_3,
        ]
