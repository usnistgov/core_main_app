"""
Template API
"""
import logging

from core_main_app.access_control.decorators import access_control
from core_main_app.commons import exceptions
from core_main_app.commons.constants import (
    TEMPLATE_FILE_EXTENSION_FOR_TEMPLATE_FORMAT,
)
from core_main_app.commons.exceptions import CoreError
from core_main_app.components.template.access_control import (
    can_read_id,
    can_write,
    get_accessible_owners,
    can_read_list,
)
from core_main_app.components.template.models import Template
from core_main_app.settings import ENABLE_JSON_SCHEMA_SUPPORT
from core_main_app.utils import json_utils as main_json_utils
from core_main_app.utils import xml as main_xml_utils
from core_main_app.utils.file import get_file_extension

logger = logging.getLogger(__name__)


@access_control(can_write)
def upsert(template, request):
    """Save or Updates the template.

    Args:
        template:
        request:

    Returns:

    """
    template_extension = get_file_extension(template.filename)
    if (
        template_extension
        == TEMPLATE_FILE_EXTENSION_FOR_TEMPLATE_FORMAT[Template.XSD]
    ):
        # Set format
        template.format = Template.XSD
        # Check if schema is valid
        main_xml_utils.is_schema_valid(template.content, request=request)
        # Set custom XSD hash
        template.hash = main_xml_utils.get_hash(template.content)
    elif (
        template_extension
        == TEMPLATE_FILE_EXTENSION_FOR_TEMPLATE_FORMAT[Template.JSON]
        and ENABLE_JSON_SCHEMA_SUPPORT
    ):
        # Set format
        template.format = Template.JSON
        # Check if schema is valid
        main_json_utils.is_schema_valid(template.content)
    else:
        # Raise an error if file extension not supported
        raise CoreError("Unsupported template extension.")
    # Save the template
    template.save_template()
    if template.format == Template.XSD:
        # Register local imports/includes for XSD templates
        _register_local_dependencies(template, request=request)
    # Return template
    return template


@access_control(can_write)
def init_template_with_dependencies(template, dependencies_dict, request):
    """Initialize template content and dependencies from a dictionary.

    Args:
        template:
        dependencies_dict:
        request:

    Returns:

    """
    if dependencies_dict is not None:
        # update template content
        template.content = (
            main_xml_utils.get_template_with_server_dependencies(
                template.content, dependencies_dict, request=request
            )
        )

    return template


@access_control(can_write)
def set_display_name(template, display_name, request):
    """Set template display name.

    Args:
        template:
        display_name:
        request:

    Returns:

    """
    # Set display name
    template.display_name = display_name
    # Save
    template.save()


@access_control(can_read_id)
def get_by_id(template_id, request):
    """Get a template.

    Args:
        template_id:
        request:

    Returns:

    """
    return Template.get_by_id(template_id)


@access_control(can_read_list)
def get_all_accessible_by_hash(template_hash, request):
    """Return all template having the given hash.

    Args:
        template_hash: Template hash
        request:

    Returns:
        List of Template instance.

    """
    return Template.get_all_by_hash(
        template_hash, users=get_accessible_owners(request=request)
    )


@access_control(can_read_list)
def get_all_accessible_by_hash_list(template_hash_list, request):
    """Return all template having the given hash list.

    Args:
        template_hash_list: Template hash list.
        request:

    Returns:
        List of Template instance.

    """
    return Template.get_all_by_hash_list(
        template_hash_list, users=get_accessible_owners(request=request)
    )


@access_control(can_read_list)
def get_all_accessible_by_id_list(template_id_list, request):
    """Returns all template with id in list

    Args:
        template_id_list:
        request:

    Returns:

    """
    return Template.get_all_by_id_list(
        template_id_list, users=get_accessible_owners(request=request)
    )


@access_control(can_read_list)
def get_all(request, is_cls=True):
    """List all templates.

    Returns:

    """
    return Template.get_all(
        is_cls, users=get_accessible_owners(request=request)
    )


@access_control(can_write)
def delete(template, request):
    """Delete the template.

    Returns:

    """
    template.delete()


def _register_local_dependencies(template, request):
    """Register local dependencies for the given template.

    Args:
        template: Template instance.

    Returns:

    """
    # Clean all dependencies. Template content could have been changed.
    template.dependencies.clear()
    # Get local dependencies
    local_dependencies = main_xml_utils.get_local_dependencies(
        template.content
    )
    if not local_dependencies:
        return

    for local_dependency in local_dependencies:
        try:
            # get the dependency
            dependency_object = get_by_id(local_dependency, request=request)
            # add the dependency
            template.dependencies.add(dependency_object)
        except exceptions.DoesNotExist as exception:
            logger.warning(
                "Dependency %s threw an exception: %s",
                local_dependency,
                str(exception),
            )
    template.save()
