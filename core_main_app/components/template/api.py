"""
Template API
"""
from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.utils.xml import is_schema_valid
from xsd_hash import xsd_hash


# TODO: exporters, xslt not added to templates
def create(template_filename, template_content, template_dependencies=None):
    """ Post the template

    :param template_filename:
    :param template_content:
    :param template_dependencies:
    :return:
    """
    is_schema_valid(template_content)
    try:
        hash_value = xsd_hash.get_hash(template_content)
    except Exception:
        raise exceptions.ApiError("Something wrong happened during the hashing of the template.")

    new_template = Template(filename=template_filename,
                            content=template_content,
                            hash=hash_value,
                            dependencies=template_dependencies).save()

    return new_template


def get(template_id):
    """
    Get a template
    :param template_id:
    :return:
    """
    try:
        return Template.get_by_id(template_id)
    except:
        raise exceptions.ApiError('No template could be found with the given id')


def get_all():
    """
    List all templates
    :return:
    """
    return Template.get_all()
