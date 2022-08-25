""" discover rules for core main app
"""
import logging

from core_main_app.permissions import rights

logger = logging.getLogger(__name__)


def init_rules(apps):
    """Init of group and permissions for the application.
    If the anonymous group does not exist, creation of the group
    If the default group does not exist, creation of the group

    Returns:

    """
    logger.info("START init rules.")

    try:
        group = apps.get_model("auth", "Group")

        # Get or Create the Group anonymous
        group.objects.get_or_create(name=rights.ANONYMOUS_GROUP)

        # Get or Create the default group
        default_group, created = group.objects.get_or_create(name=rights.DEFAULT_GROUP)

        # Get curate permissions
        permission = apps.get_model("auth", "Permission")
        publish_data_perm = permission.objects.get(codename=rights.PUBLISH_DATA)
        publish_blob_perm = permission.objects.get(codename=rights.PUBLISH_BLOB)

        # Add permissions to default group
        default_group.permissions.add(publish_data_perm)
        default_group.permissions.add(publish_blob_perm)
    except Exception as exception:
        logger.error("Impossible to init the rules: %s", str(exception))

    logger.info("FINISH init rules.")


def create_public_workspace():
    """Create and save a public workspace for registry. It will also create permissions.

    Returns:
    """
    logger.info("START create public workspace.")

    # We need the app to be ready to access the Group model
    from core_main_app.components.workspace import api as workspace_api
    from core_main_app.commons import exceptions

    try:
        try:
            # Test if global public workspace exists
            workspace_api.get_global_workspace()
        except exceptions.DoesNotExist:
            # Create workspace public global
            workspace_api.create_and_save("Global Public Workspace", is_public=True)
            logger.info("Public workspace created.")

    except Exception as exception:
        logger.error("Impossible to create global public workspace: %s", str(exception))

    logger.info("FINISH create public workspace.")
