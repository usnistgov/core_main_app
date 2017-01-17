""" discover rules for core main app
"""
from django.contrib.auth.models import Group
import core_main_app.permissions.rights as rights


def init_rules():
    """ Init of group and permissions for the application.
    If the anonymous group does not exist, creation of the group with associate permissions
    If the default group does not exist, creation of the group with associate permissions

    Returns:

    """
    try:
        # Get or Create the Group anonymous
        anonymous_group, created = Group.objects.get_or_create(name=rights.anonymous_group)
        if not created:
            anonymous_group.permissions.clear()

        # Get or Create the default group
        default_group, created = Group.objects.get_or_create(name=rights.default_group)
        if not created:
            default_group.permissions.clear()

    except Exception, e:
        print('ERROR : Impossible to init the rules : ' + e.message)
