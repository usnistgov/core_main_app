"""
Template API
"""
from core_main_app.components.template.models import Template
from core_main_app.utils.xml import is_schema_valid, get_hash, get_template_with_server_dependencies


def upsert(template):
    """Saves or Updates the template

    Args:
        template:

    Returns:

    """
    is_schema_valid(template.content)
    template.hash = get_hash(template.content)
    return template.save()


def init_template_with_dependencies(template, dependencies_dict):
    """Initializes template content and dependencies from a dict

    Args:
        template:
        dependencies_dict:

    Returns:

    """
    if dependencies_dict is not None:
        # update template content
        template.content = get_template_with_server_dependencies(template.content, dependencies_dict)
        # set the dependencies
        template.dependencies = [get(template_id) for template_id in dependencies_dict.values()]

    return template


def set_display_name(template, display_name):
    """Set template display name

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
    """Gets a template

    Args:
        template_id:

    Returns:

    """
    return Template.get_by_id(template_id)


def get_all_by_hash(template_hash):
    """ Returns all template having the given hash.

    Args:
        template_hash: Template hash.

    Returns:
        List of Template instance.

    """
    return Template.get_all_by_hash(template_hash)


def get_all_by_id_list(template_id_list):
    """ Returns all template with id in list

    Args:
        template_id_list:

    Returns:

    """
    return Template.get_all_by_id_list(template_id_list)


def get_all(is_cls=True):
    """Lists all templates

    Returns:

    """
    return Template.get_all(is_cls)


def delete(template):
    """Deletes the template

    Returns:

    """
    template.delete()
