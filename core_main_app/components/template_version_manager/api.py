"""
Template Version Manager API
"""
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager.models import TemplateVersionManager


def create_manager(template_title, template_filename, template_content, template_user=None, template_dependencies=None):
    """
    Create a new template version manager
    :param template_title:
    :param template_filename:
    :param template_content:
    :param template_user:
    :param template_dependencies:
    :return:
    """
    new_template = template_api.save(template_filename=template_filename,
                                     template_content=template_content,
                                     template_dependencies=template_dependencies)
    new_template_manager = TemplateVersionManager.create(template_title, new_template, template_user)
    return new_template_manager


def create_version(version_manager_id, template_filename, template_content, template_dependencies=None):
    """
    Create a new version of a template
    :param version_manager_id:
    :param template_filename:
    :param template_content:
    :param template_dependencies:
    :return:
    """
    template_version_manager = TemplateVersionManager.get_by_id(version_manager_id)
    new_template = template_api.save(template_filename=template_filename,
                                     template_content=template_content,
                                     template_dependencies=template_dependencies)
    template_version_manager.insert(new_template)
    return new_template


def get_global_versions():
    """
    Get all global versions of a template
    :return:
    """
    return TemplateVersionManager.get_global_versions()
