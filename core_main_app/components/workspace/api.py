""" Workspace API
"""
from core_main_app import settings
from core_main_app.access_control.decorators import access_control
from core_main_app.commons import exceptions
from core_main_app.components.group import api as group_api
from core_main_app.components.user import api as user_api
from core_main_app.components.workspace import (
    access_control as workspace_api_access_control,
)
from core_main_app.components.workspace.models import Workspace
from core_main_app.permissions import api as permission_api


def create_and_save(title, owner_id=None, is_public=False):
    """Create and save a workspace. It will also create permissions.

    Args:
        owner_id
        title
        is_public

    Returns:
    """

    # Create workspace
    workspace = _create_workspace(title, owner_id, is_public)

    try:
        workspace.save()
        return workspace
    except Exception as ex:
        # Rollback permissions
        permission_api.delete_permission(workspace.read_perm_id)
        permission_api.delete_permission(workspace.write_perm_id)
        raise exceptions.ModelError(str(ex))


def _create_workspace(title, owner_id=None, is_public=False):
    """Create workspace.

    Args:
        title
        owner_id
        is_public

    Returns:
    """
    if owner_id is None:
        return Workspace(
            title=title,
            read_perm_id=str(permission_api.create_read_perm(title, "").id),
            write_perm_id=str(permission_api.create_write_perm(title, "").id),
            is_public=is_public,
        )
    return Workspace(
        title=title,
        owner=str(owner_id),
        read_perm_id=str(permission_api.create_read_perm(title, str(owner_id)).id),
        write_perm_id=str(permission_api.create_write_perm(title, str(owner_id)).id),
        is_public=is_public,
    )


def set_title(workspace, new_title):
    """Set the workspace's title.

    Args:
        workspace
        new_title

    Returns:
    """
    workspace.title = new_title
    workspace.save()


def get_all():
    """Get all workspace.

    Returns:

    """
    return Workspace.get_all()


def get_all_by_owner(user):
    """Get all workspaces created by the given user.

    Args:
        user

    Returns:

    """
    return Workspace.get_all_by_owner(str(user.id))


def get_by_id(workspace_id):
    """Return the workspace with the given id.

    Args:
        workspace_id

    Returns:
        Workspace (obj): Workspace object with the given id

    """
    return Workspace.get_by_id(workspace_id)


def get_by_id_list(list_workspace_id):
    """Return a list of workspaces with the given id list.

    Args:
        list_workspace_id

    Returns:
    """
    list_workspace = []
    for workspace_id in list_workspace_id:
        list_workspace.append(Workspace.get_by_id(workspace_id))
    return list_workspace


def get_all_workspaces_with_read_access_by_user(user):
    """Get all workspaces with read access for the given user.

    Args:
        user

    Returns:

    """
    read_permissions = permission_api.get_all_workspace_permissions_user_can_read(user)
    return Workspace.get_all_workspaces_with_read_access_by_user_id(
        user.id, read_permissions
    )


def get_all_workspaces_with_write_access_by_user(user):
    """Get all workspaces with write access for the given user.

    Args:
        user

    Returns:

    """
    write_permissions = permission_api.get_all_workspace_permissions_user_can_write(
        user
    )
    return Workspace.get_all_workspaces_with_write_access_by_user_id(
        user.id, write_permissions
    )


def get_all_workspaces_with_read_access_not_owned_by_user(user):
    """Get the all workspaces with read access not owned by the given user.

    Args:
        user

    Returns:

    """
    read_permissions = permission_api.get_all_workspace_permissions_user_can_read(user)
    return Workspace.get_all_workspaces_with_read_access_not_owned_by_user_id(
        user.id, read_permissions
    )


def get_all_workspaces_with_write_access_not_owned_by_user_id(user):
    """Get the all workspaces with write access not owned by the given user.

    Args:
        user

    Returns:

    """
    write_permissions = permission_api.get_all_workspace_permissions_user_can_write(
        user
    )
    return Workspace.get_all_workspaces_with_write_access_not_owned_by_user_id(
        user.id, write_permissions
    )


def get_all_public_workspaces():
    """Get all public workspaces.

    Args:

    Returns:

    """
    return Workspace.get_all_public_workspaces()


def get_all_other_public_workspaces(user):
    """Get all other public workspaces.

    Args:
        user
    Returns:

    """
    return Workspace.get_all_other_public_workspaces(user.id)


def get_non_public_workspace_owned_by_user(user):
    """Get the non public workspaces owned by the given user.

    Args:
        user:

    Returns:

    """
    return Workspace.get_non_public_workspace_owned_by_user_id(user.id)


def get_public_workspaces_owned_by_user(user):
    """Get the public workspaces owned the given user.

    Args:
        user

    Returns:

    """
    return Workspace.get_public_workspaces_owned_by_user_id(user.id)


def is_workspace_public(workspace):
    """Check if the workspace is public.

    Args:
        workspace

    Return:
    """
    return workspace.is_public


def is_workspace_global(workspace):
    """Check if the workspace is global public.

    Args:
        workspace

    Return:
    """
    return workspace.is_global


def get_global_workspace():
    """Get global workspace.

    Return:
    """
    return Workspace.get_global_workspace()


def can_user_read_workspace(workspace, user):
    """Check if user has read permission on workspace.

    Args:
        workspace
        user

    Return:
    """
    if is_workspace_public(workspace):
        return True
    permission_label = permission_api.get_permission_label(workspace.read_perm_id)
    return str(workspace.owner) == str(user.id) or user.has_perm(permission_label)


def can_user_write_workspace(workspace, user):
    """Check if user has write permission on workspace.

    Args:
        workspace
        user

    Return:
    """
    permission_label = permission_api.get_permission_label(workspace.write_perm_id)
    return str(workspace.owner) == str(user.id) or user.has_perm(permission_label)


def can_group_read_workspace(workspace, group):
    """Check if group has read permission on workspace.

    Args:
        workspace
        group

    Return:
    """
    if is_workspace_public(workspace):
        return True
    permission = permission_api.get_by_id(workspace.read_perm_id)
    return permission_api.check_if_group_has_perm(group, permission)


def can_group_write_workspace(workspace, group):
    """Check if group has write permission on workspace.

    Args:
        workspace
        group

    Return:
    """
    permission = permission_api.get_by_id(workspace.write_perm_id)
    return permission_api.check_if_group_has_perm(group, permission)


def get_list_group_can_access_workspace(workspace, user):
    """Get the list of groups that have either read or write access to workspace.

    Args:
        workspace
        user

    Returns:
    """

    # List all groups that have the read permission of the workspace
    all_groups_read = get_list_group_can_read_workspace(workspace, user)

    # List all groups that have the write permission of the workspace
    all_groups_write = get_list_group_can_write_workspace(workspace, user)

    # Return the union without doublons of the two lists.
    return list(set(all_groups_read + all_groups_write))


def get_list_user_can_access_workspace(workspace, user):
    """Get the list of users that have either read or write access to workspace.

    Args:
        workspace
        user

    Returns:
    """

    # List all users that have the read permission of the workspace
    all_users_read = get_list_user_can_read_workspace(workspace, user)

    # List all users that have the write permission of the workspace
    all_users_write = get_list_user_can_write_workspace(workspace, user)

    # Return the union without doublons of the two lists.
    return list(set(all_users_read + all_users_write))


def check_if_workspace_can_be_changed(
    document, allow_change_workspace_if_public=settings.CAN_SET_PUBLIC_DATA_TO_PRIVATE
):
    """Check if a workspace of a document can be changed

    Args:
        document:
        allow_change_workspace_if_public:

    Returns:

    """
    workspace = document.workspace
    if (
        workspace is not None
        and is_workspace_public(workspace)
        and not allow_change_workspace_if_public
    ):
        return False
    return True


@access_control(workspace_api_access_control.can_user_set_workspace_public)
def set_workspace_public(workspace, user):
    """Set the workspace to public.

    Args:
        workspace
        user

    Return:
    """
    if settings.CAN_SET_WORKSPACE_PUBLIC:
        workspace.is_public = True
        workspace.save()
    else:
        raise exceptions.ApiError(
            "You can't change the state of the workspace because of the settings of the website."
        )


@access_control(workspace_api_access_control.is_workspace_owner)
def set_workspace_private(workspace, user):
    """Set the workspace to private.

    Args:
        workspace
        user

    Return:
    """
    if is_workspace_global(workspace):
        raise exceptions.ApiError("You can't change the state of the global workspace.")

    if settings.CAN_SET_PUBLIC_DATA_TO_PRIVATE:
        workspace.is_public = False
        workspace.save()
    else:
        raise exceptions.ApiError(
            "You can't change the state of the workspace because of the settings of the website."
        )


@access_control(workspace_api_access_control.can_delete_workspace)
def delete(workspace, user):
    """Delete a workspace and its permissions.

    Args:
         workspace:

    Returns:
    """

    # Can't delete a global workspace
    if workspace.is_global:
        raise exceptions.ModelError("The global workspace can not be deleted.")

    permission_api.delete_permission(workspace.read_perm_id)
    permission_api.delete_permission(workspace.write_perm_id)
    workspace.delete()


@access_control(workspace_api_access_control.is_workspace_owner)
def get_list_user_can_write_workspace(workspace, user):
    """Get list of users that have write access to workspace.

    Args:
        workspace
        user

    Return:
    """
    # Get write permission of the workspace
    write_permission = permission_api.get_by_id(workspace.write_perm_id)
    return list(write_permission.user_set.all())


@access_control(workspace_api_access_control.is_workspace_owner)
def get_list_user_can_read_workspace(workspace, user):
    """Get list of users that have read access to workspace.

    Args:
        workspace
        user

    Return:
    """

    if is_workspace_public(workspace):
        return list(user_api.get_all_users())

    # Get read permission of the workspace
    read_permission = permission_api.get_by_id(workspace.read_perm_id)

    return list(read_permission.user_set.all())


@access_control(workspace_api_access_control.is_workspace_owner)
def get_list_user_with_no_access_workspace(workspace, user):
    """Get list of users that don't have any access to the workspace.

    Args:
         workspace
         user

    Returns:
    """
    return user_api.get_all_users_except_list(
        get_list_user_can_access_workspace(workspace, user)
    )


@access_control(
    workspace_api_access_control.is_workspace_owner_to_perform_action_for_others
)
def add_user_read_access_to_workspace(workspace, new_user, user):
    """Add to new user the read access to workspace.

    Args:
          workspace
          new_user
          user
    Returns:
    """
    permission_api.add_permission_to_user(new_user, workspace.read_perm_id)


@access_control(
    workspace_api_access_control.is_workspace_owner_to_perform_action_for_others
)
def add_user_write_access_to_workspace(workspace, new_user, user):
    """Add to new user the write access to workspace.

    Args:
          workspace
          new_user
          user
    Returns:
    """
    if is_workspace_global(workspace):
        raise exceptions.ModelError(
            "You can't modify the rights of the global public workspace."
        )
    permission_api.add_permission_to_user(new_user, workspace.write_perm_id)


@access_control(
    workspace_api_access_control.is_workspace_owner_to_perform_action_for_others
)
def remove_user_read_access_to_workspace(workspace, new_user, user):
    """Remove to new user the read access to workspace.

    Args:
          workspace
          new_user
          user
    Returns:
    """
    permission_api.remove_permission_to_user(new_user, workspace.read_perm_id)


@access_control(
    workspace_api_access_control.is_workspace_owner_to_perform_action_for_others
)
def remove_user_write_access_to_workspace(workspace, new_user, user):
    """Remove to new user the write access to workspace.

    Args:
          workspace
          new_user
          user
    Returns:
    """
    if is_workspace_global(workspace):
        raise exceptions.ModelError(
            "You can't modify the rights of the global public workspace."
        )
    permission_api.remove_permission_to_user(new_user, workspace.write_perm_id)


@access_control(workspace_api_access_control.is_workspace_owner)
def get_list_group_can_write_workspace(workspace, user):
    """Get the list of groups that have write access to workspace.

    Args:
        workspace
        user

    Returns:
    """
    # Get write permission of the workspace
    write_permission = permission_api.get_by_id(workspace.write_perm_id)

    return list(write_permission.group_set.all())


@access_control(workspace_api_access_control.is_workspace_owner)
def get_list_group_can_read_workspace(workspace, user):
    """Get the list of groups that have read access to workspace.

    Args:
        workspace
        user

    Returns:
    """
    if is_workspace_public(workspace):
        return list(group_api.get_all_groups())

    # Get read permission of the workspace
    read_permission = permission_api.get_by_id(workspace.read_perm_id)

    return list(read_permission.group_set.all())


@access_control(workspace_api_access_control.is_workspace_owner)
def get_list_group_with_no_access_workspace(workspace, user):
    """Get list of groups that don't have any access to the workspace.

    Args:
         workspace
         user

    Returns:
    """
    return group_api.get_all_groups_except_list(
        get_list_group_can_access_workspace(workspace, user)
    )


@access_control(
    workspace_api_access_control.is_workspace_owner_to_perform_action_for_others
)
def add_group_read_access_to_workspace(workspace, new_group, user):
    """Add to new group the read access to workspace.

    Args:
          workspace
          new_group
          user
    Returns:
    """
    permission_api.add_permission_to_group(new_group, workspace.read_perm_id)


@access_control(
    workspace_api_access_control.is_workspace_owner_to_perform_action_for_others
)
def add_group_write_access_to_workspace(workspace, new_group, user):
    """Add to new group the write access to workspace.

    Args:
          workspace
          new_group
          user
    Returns:
    """
    if is_workspace_global(workspace):
        raise exceptions.ModelError(
            "You can't modify the rights of the global public workspace."
        )
    permission_api.add_permission_to_group(new_group, workspace.write_perm_id)


@access_control(
    workspace_api_access_control.is_workspace_owner_to_perform_action_for_others
)
def remove_group_read_access_to_workspace(workspace, group, user):
    """Remove to new group the read access to workspace.

    Args:
          workspace
          group
          user
    Returns:
    """
    permission_api.remove_permission_to_group(group, workspace.read_perm_id)


@access_control(
    workspace_api_access_control.is_workspace_owner_to_perform_action_for_others
)
def remove_group_write_access_to_workspace(workspace, group, user):
    """Remove to new group the write access to workspace.

    Args:
          workspace
          group
          user
    Returns:
    """
    if is_workspace_global(workspace):
        raise exceptions.ModelError(
            "You can't modify the rights of the global public workspace."
        )
    permission_api.remove_permission_to_group(group, workspace.write_perm_id)
