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
        default_group, created = group.objects.get_or_create(name=rights.default_group)

        # Get curate permissions
        permission = apps.get_model("auth", "Permission")
        publish_data_perm = permission.objects.get(codename=rights.publish_data)

        # Add permissions to default group
        default_group.permissions.add(publish_data_perm)

    except Exception, e:
        print('ERROR : Impossible to init the rules : ' + e.message)


def create_public_workspace():
    """ Create and save a public workspace for registry. It will also create permissions.

    Returns:
    """
    # We need the app to be ready to access the Group model
    from core_main_app.components.workspace import api as workspace_api
    from core_main_app.components.group import api as group_api
    from core_main_app.permissions import api as permission_api
    from core_main_app.commons import exceptions

    try:
        try:
            # Test if global public workspace exists
            workspace_api.get_global_workspace()
        except exceptions.DoesNotExist, dne:
            # Create workspace public global
            workspace = workspace_api.create_and_save("Global Public Workspace")

            # Set public
            permission_api.add_permission_to_group(group_api.get_anonymous_group(), workspace.read_perm_id)
            permission_api.add_permission_to_group(group_api.get_default_group(), workspace.read_perm_id)
    except Exception, e:
        print('ERROR : Impossible to create global public workspace : ' + e.message)

