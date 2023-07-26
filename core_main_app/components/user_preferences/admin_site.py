""" Custom admin site for the User Preferences model
"""

from core_main_app.utils.admin_site.model_admin_class import (
    get_base_model_admin_class,
)


class CustomUserPreferencesAdmin(
    get_base_model_admin_class("UserPreferences")
):
    """Custom User Preferences Admin"""

    list_display = [
        "user_id",
        "timezone",
    ]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding user preferences"""
        return False
