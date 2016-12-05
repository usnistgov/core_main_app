"""
Template API
"""
from core_main_app.components.template.models import Template
from core_main_app.utils.xml import is_schema_valid, get_hash


def upsert(template):
    """Saves or Updates the template

    Args:
        template:

    Returns:

    """
    is_schema_valid(template.content)
    template.hash = get_hash(template.content)
    return template.save()


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


def get_all():
    """Lists all templates

    Returns:

    """
    return Template.get_all()


def delete(template):
    """Deletes the template

    Returns:

    """
    template.delete()
