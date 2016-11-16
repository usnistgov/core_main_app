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


def get_global_version_managers():
    """Gets all global version managers of a template

    Returns:

    """
    return TemplateVersionManager.get_global_version_managers()
