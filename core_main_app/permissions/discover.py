""" discover rules for core main app
"""
import core_main_app.permissions.rights as rights


def init_rules(apps):
    """ Init of group and permissions for the application.
    If the anonymous group does not exist, creation of the group with associate permissions
    If the default group does not exist, creation of the group with associate permissions

    Returns:

    """
    try:
        group = apps.get_model("auth", "Group")
        # permission = apps.get_model("auth", "Permission")

        # Get or Create the Group anonymous
        anonymous_group, created = group.objects.get_or_create(name=rights.anonymous_group)
        if not created:
            anonymous_group.permissions.clear()

        # Get or Create the default group
        default_group, created = group.objects.get_or_create(name=rights.default_group)
        if not created:
            default_group.permissions.clear()

        # FIXME: put it back when the main model is ready
        # edit_data_perm = permission.objects.get(codename=rights.edit_data)
        # delete_data_perm = permission.objects.get(codename=rights.delete_data)
        #
        # edit_form_perm = permission.objects.get(codename=rights.edit_form)
        # delete_form_perm = permission.objects.get(codename=rights.delete_form)
        #
        # # Add permissions to default group
        # default_group.permissions.add(edit_data_perm,
        #                               delete_data_perm,
        #                               edit_form_perm,
        #                               delete_form_perm)

    except Exception, e:
        print('ERROR : Impossible to init the rules : ' + e.message)
