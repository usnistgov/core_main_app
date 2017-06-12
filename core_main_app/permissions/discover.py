""" discover rules for core main app
"""
from django.contrib.auth.models import Group, Permission
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

        edit_data_perm = Permission.objects.get(codename=rights.edit_data)
        delete_data_perm = Permission.objects.get(codename=rights.delete_data)

        edit_form_perm = Permission.objects.get(codename=rights.edit_form)
        delete_form_perm = Permission.objects.get(codename=rights.delete_form)

        # Add permissions to default group
        default_group.permissions.add(edit_data_perm,
                                      delete_data_perm,
                                      edit_form_perm,
                                      delete_form_perm)

    except Exception, e:
        print('ERROR : Impossible to init the rules : ' + e.message)
