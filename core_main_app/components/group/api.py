"""
    API for Django Groups
"""
from django.contrib.auth.models import Group
from django.db.models import Q

import core_main_app.permissions.rights as rights


def get_by_name_and_permission(name, permission_codename):
    """Get a group by name and permission codename.

    Args:
        name:
        permission_codename:

    Returns:

    """
    return Group.objects.filter(Q(name=name) & Q(permissions__codename=permission_codename))


def get_group_by_id(group_id):
    """ Return a group given its primary key.

        Args:
            group_id (str): Given group id

        Returns:
            Group object
    """
    return Group.objects.get(pk=group_id)


def get_anonymous_group():
    """ Get anonymous group of users.

    Returns:
    """
    return Group.objects.filter(name=rights.anonymous_group).first()


def get_default_group():
    """ Get default group of users.

    Returns:
    """
    return Group.objects.filter(name=rights.default_group).first()
