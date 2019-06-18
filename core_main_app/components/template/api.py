"""
Template API
"""
import logging

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.utils.xml import is_schema_valid, get_hash, \
    get_template_with_server_dependencies, get_local_dependencies

logger = logging.getLogger(__name__)


def upsert(template):
    """Save or Updates the template.

    Args:
        template:

    Returns:

    """
    # Check if schema is valid
    is_schema_valid(template.content)
    # Get hash for the template
    template.hash = get_hash(template.content)
    # Register local dependencies
    _register_local_dependencies(template)
    # Save template
    return template.save()


def init_template_with_dependencies(template, dependencies_dict):
    """Initialize template content and dependencies from a dictionary.

    Args:
        template:
        dependencies_dict:

    Returns:

    """
    if dependencies_dict is not None:
        # update template content
        template.content = get_template_with_server_dependencies(template.content, dependencies_dict)

    return template


def set_display_name(template, display_name):
    """Set template display name.

    Args:
        template:
        display_name:

    Returns:

    """
    # Set display name
    template.display_name = display_name
    # Save
    template.save()


def get(template_id):
    """Get a template.

    Args:
        template_id:

    Returns:

    """
    return Template.get_by_id(template_id)


def get_all_by_hash(template_hash):
    """ Return all template having the given hash.

    Args:
        template_hash: Template hash.

    Returns:
        List of Template instance.

    """
    return Template.get_all_by_hash(template_hash)


def get_all_by_hash_list(template_hash_list):
    """ Return all template having the given hash list.

    Args:
        template_hash_list: Template hash list.

    Returns:
        List of Template instance.

    """
    return Template.get_all_by_hash_list(template_hash_list)


def get_all_by_id_list(template_id_list):
    """ Returns all template with id in list

    Args:
        template_id_list:

    Returns:

    """
    return Template.get_all_by_id_list(template_id_list)


def get_all(is_cls=True):
    """List all templates.

    Returns:

    """
    return Template.get_all(is_cls)


def delete(template):
    """Delete the template.

    Returns:

    """
    template.delete()


def _register_local_dependencies(template):
    """ Register local dependencies for the given template.

    Args:
        template: Template instance.

    Returns:

    """
    # Clean all dependencies. Template content could have been changed.
    del template.dependencies
    # Get local dependencies
    local_dependencies = get_local_dependencies(template.content)
    for local_dependency in local_dependencies:
        try:
            # get the dependency
            dependency_object = get(local_dependency)
            # add the dependency
            template.dependencies.append(dependency_object)
        except exceptions.DoesNotExist as e:
            logger.warning("Dependency {0} throw an exception: {1}".format(local_dependency, str(e)))


def get_all_templates_by_dependencies(dependency_id_list):
    """List all templates having the given dependencies.

    Args:
        dependency_id_list: List of dependency ids.

    Returns:
        List of templates.

    """

    return Template.get_all_templates_by_dependencies(dependency_id_list)
