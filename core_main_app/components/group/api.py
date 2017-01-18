"""
    API for Django Groups
"""
from django.contrib.auth.models import Group
from django.db.models import Q


def get_by_name_and_permission(name, permission_codename):
    """Get a group by name and permission codename

    Args:
        name:
        permission_codename:

    Returns:

    """
    return Group.objects.filter(Q(name=name) & Q(permissions__codename=permission_codename))
