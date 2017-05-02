"""
Template Version Manager API
"""
from core_main_app.components.template import api as template_api
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.components.template_version_manager.models import TemplateVersionManager


def insert(template_version_manager, template):
    """Adds a version to a template version manager

    Args:
        template_version_manager:
        template:

    Returns:

    """
    # save the template in database
    saved_template = template_api.upsert(template)
    try:
        # insert the initial template in the version manager
        version_manager_api.insert_version(template_version_manager, saved_template)
        # insert the version manager in database
        return version_manager_api.upsert(template_version_manager)
    except Exception, e:
        template_api.delete(saved_template)
        raise e


def get_by_id(template_version_manager_id):
    """Gets a template version manager by its id

    Args:
        template_version_manager_id: Id.

    Returns:

    """
    return TemplateVersionManager.get_by_id(template_version_manager_id)


def get_global_version_managers(_cls=True):
    """Gets all global version managers of a template

    Returns:
        _cls:
    """
    return TemplateVersionManager.get_global_version_managers(_cls)


def get_active_global_version_manager(_cls=True):
    """ Returns all active Version Managers with user set to None

    Returns:

    """
    return TemplateVersionManager.get_active_global_version_manager(_cls)


def get_disable_global_version_manager(_cls=True):
    """ Returns all disabled Version Managers with user set to None

    Returns:

    """
    return TemplateVersionManager.get_disable_global_version_manager(_cls)


def get_active_version_manager_by_user_id(user_id, _cls=True):
    """ Returns all active Version Managers with given user id

    Returns:

    """
    return TemplateVersionManager.get_active_version_manager_by_user_id(user_id, _cls)


def get_disable_version_manager_by_user_id(user_id, _cls=True):
    """ Returns all disabled Version Managers with given user id

    Returns:

    """
    return TemplateVersionManager.get_disable_version_manager_by_user_id(user_id, _cls)


def get_version_number(template_version_manager, template):
    """ Returns version number from version id.

    Args:
        template_version_manager:
        template:

    Returns:
        Version number

    """
    return template_version_manager.get_version_number(template)


def get_all_by_version_ids(version_ids):
    """Gets all template version managers by a list of version ids.

    Args:
        version_ids: list of version ids.

    Returns:
        List of template version managers.

    """
    return TemplateVersionManager.get_all_by_version_ids(version_ids)
