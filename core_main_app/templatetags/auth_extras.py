"""Template tag to check user permission
"""

from django import template

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.access_control.utils import check_has_perm

register = template.Library()


@register.filter(name="has_perm")
def has_perm(user, permission):
    """Check if user has the right level of permission to access a feature.

    Args:
        user:
        permission:

    Returns:
        bool: Whether the user has the permission or not.
    """
    try:
        permission_name = permission.split(".")[1]
        check_has_perm(user, permission_name)
        return True
    except AccessControlError:
        return False
