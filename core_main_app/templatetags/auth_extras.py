"""Template tag to check user permission
"""

from django import template

from core_main_app.permissions import rights as RIGHTS
from core_main_app.components.group import api as group_api

register = template.Library()


@register.filter(name="has_perm")
def has_perm(user, permission):
    """Check if user has the right level of permission to access a feature.

    Args:
        user:
        permission:

    Returns:

    """
    try:
        permission_split = permission.split(".")
        permission_name = permission_split[1]

        if user.is_anonymous:
            # We can give directly the permission name
            access = group_api.get_by_name_and_permission(
                name=RIGHTS.ANONYMOUS_GROUP, permission_codename=permission_name
            )
        else:
            # We need to prefix with the app name
            access = user.has_perm(permission)
    except:
        # If something went wrong, we ask for an empty permission to give the access if it's a superUser
        access = user.has_perm("")

    return access
