""" Template access control
"""
from django.db.models import Q

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.template.models import Template
from django.conf import settings
from core_main_app.utils.requests_utils.access_control import (
    get_request_from_args,
)


def check_can_read_template(template, user):
    if user.is_superuser:  # No checks for superuser
        return

    # Anonymous user
    if user.is_anonymous:
        if template.user:
            raise AccessControlError(
                "Template: The user doesn't have enough rights."
            )
        if not settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
            raise AccessControlError(
                "Template: The user doesn't have enough rights."
            )

    # Registered user
    if template.user and template.user != str(user.id):
        raise AccessControlError(
            "Template: The user doesn't have enough rights."
        )


def can_read_id(func, template_id, request):
    """Can read document.

    Args:
        func:
        template_id:
        request:

    Returns:

    """
    # Retrieve request and document from args
    request = get_request_from_args(template_id, request=request)
    template = func(template_id, request=request)

    # Verify that user can read the template and return the object
    check_can_read_template(template, request.user)
    return template


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
        if not settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
            raise AccessControlError(
                "Template: The user doesn't have enough rights."
            )
    return func(*args, **kwargs)


def can_write(func, *args, **kwargs):
    """Can write template.

    Args:
        func:
        args:
        kwargs:

    Returns:

    """

    template = next((arg for arg in args if isinstance(arg, Template)), None)

    check_can_write(template, *args, **kwargs)

    return func(*args, **kwargs)


def get_accessible_owners(request):
    """Get a list of templates owners, the user can read from

    Args:
        request:

    Returns:

    """
    if not request or request.user.is_anonymous:
        if settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
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
            if not settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
                raise AccessControlError(
                    "Template: The user doesn't have enough rights."
                )

        # user is set
        if template.user and template.user != str(request.user.id):
            raise AccessControlError(
                "Template: The user doesn't have enough rights."
            )

    return document_list


def check_can_write(template, *args, **kwargs):
    """Check can write template.

    Args:
        template:
        args:
        kwargs:

    Returns:

    """
    request = get_request_from_args(*args, **kwargs)

    # super user
    if request.user.is_superuser:
        return True

    # anonymous
    if request.user.is_anonymous:
        raise AccessControlError(
            "Template: The user doesn't have enough rights."
        )

    # user is set
    if template.user:
        if template.user == str(request.user.id):
            return True
    # user is not set
    else:
        if request.user.is_staff:
            return True

    raise AccessControlError("Template: The user doesn't have enough rights.")
