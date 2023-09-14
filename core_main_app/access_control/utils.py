""" Access control utilities for core_main_app.
"""
import logging

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.group import api as group_api
from core_main_app.permissions import api as permissions_api, rights

logger = logging.getLogger(__name__)


def check_has_perm(user, permission_name):
    """Check that a user has a specific permission

    Args:
        user - User: User object.
        permission_name - str: Codename of the permission.

    Raises:
        AccessControlError - If the user does not have the permission
    """
    if user.is_superuser:  # Superusers are always authorized.
        return

    try:
        permission_object = permissions_api.get_by_codename(permission_name)

        # User is anonymous, check that the anonymous group has the permission.
        if user.is_anonymous:
            has_access = group_api.get_by_name_and_permission(
                name=rights.ANONYMOUS_GROUP,
                permission_codename=permission_name,
            )
        else:  # User is registered, check that the user is authorized.
            has_access = user.has_perm(
                f"{permission_object.content_type.app_label}."
                f"{permission_object.codename}"
            )
    except Exception as exc:  # noqa, pylint: disable=broad-except
        # If an exception occurs while checking the permission, deny access and log the
        # exception message.
        logger.warning(
            "Exception raised while executing `check_has_perm`: %s", str(exc)
        )
        has_access = False

    # Raise an exception if the user does not have the proper permission.
    if not has_access:
        raise AccessControlError(
            "The user does not have enough rights to perform this action."
        )
