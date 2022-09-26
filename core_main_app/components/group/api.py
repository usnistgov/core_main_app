"""
    API for Django Groups
"""
from django.contrib.auth.models import Group
from django.db.models import Q

from core_main_app.permissions import rights


def get_or_create(name):
    """Get or create a group.
    Args:
        name:

    Returns:
    """
    group, created = Group.objects.get_or_create(name=name)
    return group, created


def get_all_groups():
    """Return all Groups.

    Returns:
        List of Groups

    """
    return Group.objects.all()


def get_by_name_and_permission(name, permission_codename):
    """Get a group by name and permission codename.

    Args:
        name:
        permission_codename:

    Returns:

    """
    return Group.objects.filter(
        Q(name=name) & Q(permissions__codename=permission_codename)
    )


def get_group_by_id(group_id):
    """Return a group given its primary key.

    Args:
        group_id (str): Given group id

    Returns:
        Group object
    """
    return Group.objects.get(pk=group_id)


def get_anonymous_group():
    """Get anonymous group of users.

    Returns:
    """
    return Group.objects.filter(name=rights.ANONYMOUS_GROUP).first()


def get_default_group():
    """Get default group of users.

    Returns:
    """
    return Group.objects.filter(name=rights.DEFAULT_GROUP).first()


def get_all_groups_by_list_id(list_groups_ids):
    """Get all groups by the given list of group ids.

    Args:
        list_groups_ids

    Returns:
    """
    return Group.objects.filter(id__in=list_groups_ids)


def get_all_groups_except_list_id(list_groups_ids):
    """Get all groups except the given list of group ids.

    Args:
        list_groups_ids

    Returns:
    """
    return Group.objects.exclude(id__in=list_groups_ids)


def get_all_groups_except_list(list_group):
    """Get all groups except the given list of groups.

    Args:
        list_group

    Returns:
    """
    return get_all_groups_except_list_id(
        [str(group.id) for group in list_group]
    )
