""" Set of functions to define the rules for access control
"""
import logging

import core_main_app.permissions.rights as rights
from core_main_app.access_control.api import has_perm_publish, can_write_in_workspace

logger = logging.getLogger(__name__)


def has_perm_publish_blob(user):
    """Does the user have the permission to publish a blob.

    Args:
        user

    Returns
    """
    has_perm_publish(user, rights.publish_blob)


def can_write_blob_workspace(func, data, workspace, user):
    """Can user write data in workspace.

    Args:
        func:
        data:
        workspace:
        user:

    Returns:

    """
    return can_write_in_workspace(func, data, workspace, user, rights.publish_blob)
