""" Access control utilities for core_main_app.
"""
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.permissions import api as permissions_api


def check_has_perm(user, permission_name):
    """Check that a user has a specific permission

    Args:
        user - User: User object.
        permission_name - str: Codename of the permission.

    Raises:
        AccessControlError - If the user does not have the permission
    """
    if user.is_superuser:  # Superuser always has the permission.
        return

    permission_object = permissions_api.get_by_codename(permission_name)
    if not user.has_perm(
        f"{permission_object.content_type.app_label}."
        f"{permission_object.codename}"
    ):
        raise AccessControlError(
            "The user does not have enough rights to perform this action."
        )
