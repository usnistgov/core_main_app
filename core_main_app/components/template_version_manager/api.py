"""
Template Version Manager API
"""
from core_main_app.access_control.api import is_superuser
from core_main_app.access_control.decorators import access_control
from core_main_app.commons import exceptions
from core_main_app.components.template import api as template_api
from core_main_app.components.template.access_control import can_read, can_read_global
from core_main_app.components.template_version_manager.access_control import can_write
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.components.version_manager.access_control import can_read_list
from core_main_app.components.version_manager.utils import (
    get_latest_version_name,
    get_version_name,
)


@access_control(can_read)
def get_by_id(version_manager_id, request):
    """Get a template version manager by its id.

    Args:
        version_manager_id:
        request:

    Returns:

    """
    return TemplateVersionManager.get_by_id(version_manager_id)


@access_control(can_write)
def insert(template_version_manager, template, request):
    """Add a version to a template version manager.

    Args:
        template_version_manager:
        template:
        request:

    Returns:

    """
    # save the template in database
    template_api.upsert(template, request=request)
    try:
        # create a version manager
        version_manager_api.upsert(template_version_manager, request=request)
        # set version manager
        template.version_manager = template_version_manager
        # set current version
        if len(template_version_manager.versions) == 0:
            template.is_current = True
        # update template
        template.display_name = get_latest_version_name(template_version_manager)
        # save template
        template.save_template()
        # return version manager
        return template_version_manager
    except Exception as exception:
        template.delete()
        raise exception


@access_control(can_write)
def edit_title(template_version_manager, title, request):
    """Edit template version manager title.

    Args:
        template_version_manager:
        title:
        request:

    Returns:

    """
    # set version template manager title
    template_version_manager.title = title
    # save template version manager
    template_version_manager.save_template_version_manager()
    # update templates display names
    _update_templates_display_name(template_version_manager, request=request)


def _update_templates_display_name(template_version_manager, request):
    """Update templates display name.

    Args:
        template_version_manager:
        request:

    Returns:

    """
    # Iterate versions
    for i in range(0, len(template_version_manager.versions)):
        # get template id from list of versions
        template_id = template_version_manager.versions[i]
        # get template from template id
        template = template_api.get_by_id(template_id, request=request)
        # get display name for the template
        display_name = get_version_name(template_version_manager.title, i + 1)
        # update template's display name
        template_api.set_display_name(template, display_name, request=request)


@access_control(can_read_global)
def get_global_version_managers(request, _cls=True):
    """Get all global version managers of a template.

    Args:
        request:
        _cls:

    Returns:

    """
    return TemplateVersionManager.get_global_version_managers(_cls)


@access_control(can_read_global)
def get_active_global_version_manager(request, _cls=True):
    """Return all active Version Managers with user set to None.

    Args:
        request:
        _cls:

    Returns:

    """
    return TemplateVersionManager.get_active_global_version_manager(_cls)


# NOTE: access control, filter by user in request
def get_active_version_manager_by_user_id(request, _cls=True):
    """Return all active Version Managers with given user id.

    Returns:

    """
    return TemplateVersionManager.get_active_version_manager_by_user_id(
        str(request.user.id), _cls
    )


# NOTE: access control, filter by user in request
def get_all_by_user_id(request, _cls=True):
    """Return all Template Version Managers with given user id.

    Returns:

    """
    return TemplateVersionManager.get_all_version_manager_by_user_id(
        str(request.user.id), _cls
    )


@access_control(is_superuser)
def get_all(request, _cls=True):
    """Return all Template Version Managers.

    Returns:

    """
    return TemplateVersionManager.get_all_version_manager(_cls)


@access_control(can_read_list)
def get_by_id_list(list_id, request):
    """Get a version managers with the given id list.

    Args:
        list_id:
        request

    Returns:

    """
    return TemplateVersionManager.get_by_id_list(list_id)


@access_control(can_read_global)
def get_active_global_version_manager_by_title(version_manager_title, request):
    """Return active Version Manager by its title with user set to None.

    Args:
        version_manager_title: Version Manager title
        request:

    Returns:
        Version Manager instance

    """
    return TemplateVersionManager.get_active_global_version_manager_by_title(
        version_manager_title
    )
