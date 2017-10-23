""" discover rules for core main app
"""
import core_main_app.permissions.rights as rights


def init_rules(apps):
    """ Init of group and permissions for the application.
    If the anonymous group does not exist, creation of the group
    If the default group does not exist, creation of the group

    Returns:

    """
    try:
        group = apps.get_model("auth", "Group")

        # Get or Create the Group anonymous
        group.objects.get_or_create(name=rights.anonymous_group)

        # Get or Create the default group
        group.objects.get_or_create(name=rights.default_group)

    except Exception, e:
        print('ERROR : Impossible to init the rules : ' + e.message)
