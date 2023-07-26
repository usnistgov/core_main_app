""" User Preferences API
"""

from core_main_app.access_control.decorators import access_control
from core_main_app.components.user_preferences.access_control import (
    can_write,
    can_read,
)
from core_main_app.components.user_preferences.models import UserPreferences


@access_control(can_write)
def upsert(user_preferences, user):
    """Save or update the user preferences.

    Args:
        user_preferences:
        user:

    Returns:

    """

    user_preferences.save_object()
    return user_preferences


@access_control(can_write)
def delete(user_preferences, user):
    """Delete the user preferences.

    Args:
        user_preferences:
        user:

    Returns:

    """
    # delete user preferences in database
    return user_preferences.delete()


@access_control(can_read)
def get_by_user(user):
    """Return User Preferences by user.

    Args:
        user: User

    Returns:
        user preferences user id.

    """
    return UserPreferences.get_by_user(user)
