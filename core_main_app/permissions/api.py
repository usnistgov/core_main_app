"""
Permissions API
"""
import logging

from django.contrib.auth.models import Permission, ContentType
from django.db import IntegrityError
from django.db.models import Q

from core_main_app.commons import exceptions
from core_main_app.components.group import api as group_api
from core_main_app.permissions.rights import (
    CAN_READ_NAME,
    CAN_READ_CODENAME,
    CONTENT_TYPE_APP_LABEL,
    CAN_WRITE_NAME,
    CAN_WRITE_CODENAME,
)

logger = logging.getLogger(__name__)


def _title_to_codename(title):
    """Change the title to a codename.

    Args:
        title:

    Returns:
    """

    # remove unnecessary spaces
    title = title.strip()
    # to lower case
    title = title.lower()
    # replace spaces by underscores
    title = title.replace(" ", "_")
    return title


def create_read_perm(title, owner_id):
    """Create read permission.

    Args:
        title
        owner_id

    Returns:
    """
    name = CAN_READ_NAME + " - " + title.strip() + " (" + owner_id + ")"
    content_type = ContentType.objects.get(
        app_label=CONTENT_TYPE_APP_LABEL, model="main"
    )
    codename = (
        CAN_READ_CODENAME + "_" + _title_to_codename(title) + " (" + owner_id + ")"
    )
    return _create_perm(name, content_type, codename)


def create_write_perm(title, owner_id):
    """Create write permission.

    Args:
        title
        owner_id

    Returns:
    """
    name = CAN_WRITE_NAME + " - " + title.strip() + " (" + owner_id + ")"
    content_type = ContentType.objects.get(
        app_label=CONTENT_TYPE_APP_LABEL, model="main"
    )
    codename = (
        CAN_WRITE_CODENAME + "_" + _title_to_codename(title) + " (" + owner_id + ")"
    )
    return _create_perm(name, content_type, codename)


def _create_perm(name, content_type, codename):
    """Create permission.

    Args:
        name
        content_type
        codename

    Returns:
    """

    try:
        perm, created = Permission.objects.get_or_create(
            name=name, content_type=content_type, codename=codename
        )
    except IntegrityError:
        raise exceptions.NotUniqueError("The permission already exists.")
    except Exception:
        raise exceptions.ModelError("Problem while creating the permission.")

    if not created:
        raise exceptions.NotUniqueError("The permission already exists.")
    return perm


def add_permission_to_user(user, permission):
    """Add permission to user.

    Args:
        user_id
        permission

    Returns:
    """
    user.user_permissions.add(permission)
    user.save()


def add_permission_to_group(group, permission):
    """Add permission to group.

    Args:
        group
        permission

    Returns:
    """
    group.permissions.add(permission)
    group.save()


def remove_permission_to_user(user, permission):
    """Remove permission from user.

    Args:
        user
        permission

    Returns:
    """
    user.user_permissions.remove(permission)
    user.save()


def remove_permission_to_group(group, permission):
    """Remove permission from group.

    Args:
        group
        permission

    Returns:
    """
    group.permissions.remove(permission)
    group.save()


def get_all_workspace_permissions_user_can_write(user):
    """Get a list of permission ids of workspaces that the user has write access.

    Args:
        user

    Return:

    """
    # TODO: fix the super user case
    if user.is_superuser:
        return [
            str(perm.id)
            for perm in Permission.objects.filter(
                content_type__app_label=CONTENT_TYPE_APP_LABEL,
                codename__startswith=CAN_WRITE_CODENAME,
            )
        ]
    if user.is_anonymous:
        # No permissions.
        return []
    return [
        str(perm.id)
        for perm in Permission.objects.filter(
            (Q(user=user) | Q(group__in=user.groups.all())),
            content_type__app_label=CONTENT_TYPE_APP_LABEL,
            codename__startswith=CAN_WRITE_CODENAME,
        )
    ]


def get_all_workspace_permissions_user_can_read(user):
    """Get a list of permission ids of workspaces that the user has read access.

    Args:
        user

    Return:
    """
    # TODO: fix the super user case
    if user.is_superuser:
        return [
            str(perm.id)
            for perm in Permission.objects.filter(
                content_type__app_label=CONTENT_TYPE_APP_LABEL,
                codename__startswith=CAN_READ_CODENAME,
            )
        ]
    if user.is_anonymous:
        return [
            str(perm.id)
            for perm in Permission.objects.filter(
                group=group_api.get_anonymous_group(),
                content_type__app_label=CONTENT_TYPE_APP_LABEL,
                codename__startswith=CAN_READ_CODENAME,
            )
        ]
    return [
        str(perm.id)
        for perm in Permission.objects.filter(
            (Q(user=user) | Q(group__in=user.groups.all())),
            content_type__app_label=CONTENT_TYPE_APP_LABEL,
            codename__startswith=CAN_READ_CODENAME,
        )
    ]


def get_by_id(permission_id):
    """Get the permission by id.

    Args:
         permission_id:
    Returns:
    """
    return Permission.objects.get(pk=permission_id)


def delete_permission(permission_id):
    """Delete a permission.

    Args:
        permission_id:

    Return:
    """

    try:
        perm = get_by_id(permission_id)
        perm.delete()
    except Exception as exception:
        logger.warning("delete_permission threw an exception: %s", str(exception))


def get_permission_label(permission_id):
    """Get the label of a permission.

    Args:
        permission_id:

    Return:
    """
    permission = Permission.objects.get(pk=permission_id)
    return permission.content_type.app_label + "." + permission.codename


def check_if_group_has_perm(group, permission):
    """Check if group has permission.

    Args:
        group:
        permission:
    Returns:
    """
    return len(group.permissions.filter(id=str(permission.id))) == 1


def get_by_codename(codename):
    """Get the permission by codename.

    Args:
         codename:
    Returns:
    """
    return Permission.objects.get(codename=codename)
