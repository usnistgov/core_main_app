"""
Template Version Manager API
"""
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager.models import TemplateVersionManager
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.components.version_manager.utils import get_latest_version_name, get_version_name


def insert(template_version_manager, template):
    """Add a version to a template version manager.

    Args:
        template_version_manager:
        template:

    Returns:

    """
    # save the template in database
    template_api.upsert(template)
    try:
        # insert the initial template in the version manager
        version_manager_api.insert_version(template_version_manager, template)
        # insert the version manager in database
        version_manager_api.upsert(template_version_manager)
        # get template display name
        display_name = get_latest_version_name(template_version_manager)
        # update saved template
        template_api.set_display_name(template, display_name)
        # return version manager
        return template_version_manager
    except Exception as e:
        template_api.delete(template)
        raise e


def edit_title(template_version_manager, title):
    """Edit template version manager title.

    Args:
        template_version_manager:
        title:

    Returns:

    """
    # set version template manager title
    template_version_manager.title = title
    # save template version manager
    template_version_manager.save_template_version_manager()
    # update templates display names
    update_templates_display_name(template_version_manager)


def update_templates_display_name(template_version_manager):
    """Update templates display name.

    Args:
        template_version_manager:

    Returns:

    """
    # Iterate versions
    for i in range(0, len(template_version_manager.versions)):
        # get template id from list of versions
        template_id = template_version_manager.versions[i]
        # get template from template id
        template = template_api.get(template_id)
        # get display name for the template
        display_name = get_version_name(template_version_manager.title, i+1)
        # update template's display name
        template_api.set_display_name(template, display_name)


def get_by_id(template_version_manager_id):
    """Get a template version manager by its id.

    Args:
        template_version_manager_id: Id.

    Returns:

    """
    return TemplateVersionManager.get_by_id(template_version_manager_id)


def get_global_version_managers(_cls=True):
    """Get all global version managers of a template.

    Returns:
        _cls:
    """
    return TemplateVersionManager.get_global_version_managers(_cls)


def get_active_global_version_manager(_cls=True):
    """ Return all active Version Managers with user set to None.

    Returns:

    """
    return TemplateVersionManager.get_active_global_version_manager(_cls)


def get_disable_global_version_manager(_cls=True):
    """ Return all disabled Version Managers with user set to None.

    Returns:

    """
    return TemplateVersionManager.get_disable_global_version_manager(_cls)


def get_active_version_manager_by_user_id(user_id, _cls=True):
    """ Return all active Version Managers with given user id.

    Returns:

    """
    return TemplateVersionManager.get_active_version_manager_by_user_id(user_id, _cls)


def get_disable_version_manager_by_user_id(user_id, _cls=True):
    """ Return all disabled Version Managers with given user id.

    Returns:

    """
    return TemplateVersionManager.get_disable_version_manager_by_user_id(user_id, _cls)


def get_version_number(template_version_manager, template):
    """ Return version number from version id.

    Args:
        template_version_manager:
        template:

    Returns:
        Version number

    """
    return template_version_manager.get_version_number(template)


def get_by_version_id(version_id):
    """Get the template version manager containing the given version id.

    Args:
        version_id: version id.

    Returns:
        template version manager.

    """
    return TemplateVersionManager.get_by_version_id(version_id)


def get_all_by_version_ids(version_ids):
    """Get all template version managers by a list of version ids.

    Args:
        version_ids: list of version ids.

    Returns:
        List of template version managers.

    """
    return TemplateVersionManager.get_all_by_version_ids(version_ids)


def get_all_version_manager_except_user_id(user_id, _cls=True):
    """ Return all  Version Managers of all users except user with given user id.

    Returns:

    """
    return TemplateVersionManager.get_all_version_manager_except_user_id(user_id, _cls)


def get_all_by_user_id(user_id, _cls=True):
    """ Return all Template Version Managers with given user id.

    Returns:

    """
    return TemplateVersionManager.get_all_version_manager_by_user_id(user_id, _cls)


def get_all(_cls=True):
    """ Return all Template Version Managers.

    Returns:

    """
    return TemplateVersionManager.get_all_version_manager(_cls)
