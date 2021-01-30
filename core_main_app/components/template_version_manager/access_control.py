""" Template Version Manager Access Control
"""

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.utils.requests_utils.access_control import (
    get_request_from_args,
)


def can_write(func, *args, **kwargs):
    """Can write template.

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

    # anonymous cannot write
    if request.user.is_anonymous:
        raise AccessControlError("Template VM: The user doesn't have enough rights.")

    template_version_manager = next(
        (arg for arg in args if isinstance(arg, TemplateVersionManager)), None
    )

    # user is set
    if template_version_manager.user:
        if template_version_manager.user == str(request.user.id):
            return func(*args, **kwargs)
    # user is not set
    else:
        if request.user.is_staff:
            return func(*args, **kwargs)

    raise AccessControlError("Template VM: The user doesn't have enough rights.")
