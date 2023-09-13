""" User preferences Access Control
"""
from django.contrib.auth.models import AnonymousUser, User

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.user_preferences.models import UserPreferences


def can_write(func, *args, **kwargs):
    """Can write user preferences.

    Args:
        func:
        args:
        kwargs:

    Returns:

    """
    user = next(
        (arg for arg in args if isinstance(arg, (User, AnonymousUser))),
        None,
    )

    # anonymous cannot write
    if not user or user.is_anonymous:
        raise AccessControlError(
            "The user doesn't have enough rights to edit these preferences."
        )

    # super user
    if user.is_superuser:
        return func(*args, **kwargs)

    document = next(
        (arg for arg in args if isinstance(arg, UserPreferences)), None
    )
    if document.user_id != str(user.id):
        raise AccessControlError(
            "The user doesn't have enough rights to edit these preferences."
        )

    return func(*args, **kwargs)


def can_read(func, user):
    """Can read user preferences.

    Args:
        func:
        user:

    Returns:

    """
    # If anon, raise error
    if user is None or isinstance(user, AnonymousUser):
        raise AccessControlError(
            "The user doesn't have enough rights to access these preferences."
        )

    # If user is superuser return func
    if user.is_superuser:
        return func(user)

    # Get user preferences
    user_preferences = func(user)

    # If user preferences don't belong to user
    if user_preferences.user_id != str(user.id):
        raise AccessControlError(
            "The user doesn't have enough rights to access these preferences."
        )

    # Return preferences
    return user_preferences
