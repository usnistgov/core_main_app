""" Template access control
"""
from django.db.models import Q

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.template.models import Template
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
            raise AccessControlError("Template: The user doesn't have enough rights.")
        if not CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
            raise AccessControlError("Template: The user doesn't have enough rights.")

    # user is set
    if document.user and document.user != str(request.user.id):
        raise AccessControlError("Template: The user doesn't have enough rights.")

    return document


def can_read_global(func, *args, **kwargs):
    """Can read global template

    Args:
        func:
        *args:
        **kwargs:

    Returns:

    """
    request = get_request_from_args(*args, **kwargs)
    if request.user.is_anonymous:
        if not CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
            raise AccessControlError("Template: The user doesn't have enough rights.")
    return func(*args, **kwargs)


def can_write(func, *args, **kwargs):
    """Can write template.

    Args:
        func:
        args:
        kwargs:

    Returns:

    """
    request = get_request_from_args(*args, **kwargs)

    template = next((arg for arg in args if isinstance(arg, Template)), None)

    # super user
    if request.user.is_superuser:
        return func(*args, **kwargs)

    # anonymous
    if request.user.is_anonymous:
        raise AccessControlError("Template: The user doesn't have enough rights.")

    # user is set
    if template.user:
        if template.user == str(request.user.id):
            return func(*args, **kwargs)
    # user is not set
    else:
        if request.user.is_staff:
            return func(*args, **kwargs)

    raise AccessControlError("Template: The user doesn't have enough rights.")


def get_accessible_owners(request):
    """Get a list of templates owners, the user can read from

    Args:
        request:

    Returns:

    """
    if not request or request.user.is_anonymous:
        if CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
            # global templates only
            return Q(user__isnull=True)
        # nothing
        return Q(user__in=[])
    if request.user.is_superuser:
        # no restrictions
        return None
    # global and owned templates
    in_q_list = Q()
    in_q_list |= Q(user__isnull=True)
    in_q_list |= Q(user=str(request.user.id))
    return in_q_list


def can_read_list(func, *args, **kwargs):
    """Can read list of version managers.

    Args:
        func:

    Returns:

    """
    request = get_request_from_args(*args, **kwargs)
    # super user
    if request and request.user.is_superuser:
        return func(*args, **kwargs)

    document_list = func(*args, **kwargs)
    for template in document_list:
        # anonymous user
        if not request or request.user.is_anonymous:
            if template.user:
                raise AccessControlError(
                    "Template: The user doesn't have enough rights."
                )
            if not CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
                raise AccessControlError(
                    "Template: The user doesn't have enough rights."
                )

        # user is set
        if template.user and template.user != str(request.user.id):
            raise AccessControlError("Template: The user doesn't have enough rights.")

    return document_list
