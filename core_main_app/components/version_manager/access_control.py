""" Version Manager Access Control
"""

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.version_manager.models import VersionManager, Version
from core_main_app.settings import CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT
from core_main_app.utils.requests_utils.access_control import (
    get_request_from_args,
)


def can_read(func, document_id, request):
    """Can read document.

    Args:
        func:
        document_id:
        request:

    Returns:

    """
    request = get_request_from_args(document_id, request=request)

    # super user
    if request.user.is_superuser:
        return func(document_id, request=request)

    # get the document
    document = func(document_id, request=request)

    # anonymous user
    if request.user.is_anonymous:
        if document.user:
            raise AccessControlError(
                "Version Manager: The user doesn't have enough rights."
            )
        if not CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
            raise AccessControlError(
                "Version Manager: The user doesn't have enough rights."
            )

    # user is set
    if document.user and document.user != str(request.user.id):
        raise AccessControlError(
            "Version Manager: The user doesn't have enough rights."
        )

    return document


def can_write(func, *args, **kwargs):
    """Can write version_manager.

    Args:
        func:
        args:
        kwargs:

    Returns:

    """
    request = get_request_from_args(*args, **kwargs)

    # super user
    if request.user.is_superuser:
        return func(*args, **kwargs)

    # anonymous
    if request.user.is_anonymous:
        raise AccessControlError(
            "Version Manager: The user doesn't have enough rights."
        )

    object_to_check = next(
        (arg for arg in args if isinstance(arg, (VersionManager, Version))),
        None,
    )

    # user is set
    if object_to_check.user:
        if object_to_check.user == str(request.user.id):
            return func(*args, **kwargs)
    # user is not set
    else:
        if request.user.is_staff:
            return func(*args, **kwargs)

    raise AccessControlError("Version Manager: The user doesn't have enough rights.")


def can_read_list(func, list_id, request):
    """Can read list of version managers.

    Args:
        func:
        list_id:
        request:

    Returns:

    """
    # super user
    if request.user.is_superuser:
        return func(list_id, request=request)

    document_list = func(list_id, request)
    for version_manager in document_list:
        # anonymous user
        if request.user.is_anonymous:
            if version_manager.user:
                raise AccessControlError(
                    "Version Manager: The user doesn't have enough rights."
                )
            if not CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
                raise AccessControlError(
                    "Version Manager: The user doesn't have enough rights."
                )

        # user is set
        if version_manager.user and version_manager.user != str(request.user.id):
            raise AccessControlError(
                "Version Manager: The user doesn't have enough rights."
            )

    return document_list


def can_read_global(func, *args, **kwargs):
    """Can read global version managers.

    Args:
        func:
        *args:
        **kwargs:

    Returns:

    """
    request = get_request_from_args(*args, **kwargs)
    if request.user.is_anonymous:
        if not CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
            raise AccessControlError(
                "Version Manager: The user doesn't have enough rights."
            )
    return func(*args, **kwargs)


def can_read_version_manager(func, version_manager, version, request):
    """Can read global version managers.

    Args:
        func:
        version_manager:
        version:
        request:

    Returns:

    """
    request = get_request_from_args(version_manager, version, request=request)

    if request.user.is_superuser:
        return func(version_manager, version, request=request)
    # anonymous user
    if request.user.is_anonymous:
        if version_manager.user:
            raise AccessControlError(
                "Version Manager: The user doesn't have enough rights."
            )
        if not CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
            raise AccessControlError(
                "Version Manager: The user doesn't have enough rights."
            )

    # user is set
    if version_manager.user and version_manager.user != str(request.user.id):
        raise AccessControlError(
            "Version Manager: The user doesn't have enough rights."
        )

    return func(version_manager, version, request=request)
