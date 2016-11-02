"""
Template API
"""

from core_main_app.commons.exceptions import MDCSError
from core_main_app.components.template.models import Template
from core_main_app.utils.xml import is_schema_valid
from xsd_hash import xsd_hash


# TODO: exporters, xslt not added to templates
def template_post(template_filename, template_content, template_dependencies=[]):
    """
    Post the template
    :param template_filename:
    :param template_content:
    :param template_dependencies:
    :return:
    """
    is_schema_valid(template_content)
    try:
        hash_value = xsd_hash.get_hash(template_content)
    except Exception:
        raise MDCSError("Something wrong happened during the hashing of the template.")
    new_template = Template.create_template(template_filename=template_filename,
                                            template_content=template_content,
                                            template_hash=hash_value,
                                            template_dependencies=template_dependencies)

    return new_template


def template_get(template_id):
    """
    Get a template
    :param template_id:
    :return:
    """
    try:
        return Template.get_by_id(template_id)
    except:
        raise MDCSError('No template could be found with the given id')


def template_list():
    """
    List all templates
    :return:
    """
    return Template.get_all()
