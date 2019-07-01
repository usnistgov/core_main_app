""" Utils for template version manager rest Apis
"""
import json

from core_main_app.commons.exceptions import RestApiError
from core_main_app.access_control.exceptions import AccessControlError


def load_dependencies(validated_data):
    """Return dependencies as a dict.

    Args:
        validated_data:

    Returns:

    """
    if 'dependencies_dict' in validated_data:
        dependencies_dict = validated_data['dependencies_dict']
        try:
            return json.loads(dependencies_dict)
        except:
            raise RestApiError('Incorrect format of the dependencies parameter.')
    return None


def can_user_modify_template_version_manager(template_version_manager, user):
    """ Check that user can modify the template version manager.

    Args:
        template_version_manager:
        user:

    Returns:

    """
    if user.is_superuser is False and user.is_staff is False:
        if template_version_manager.user != user.id:
            raise AccessControlError("You don't have the permission to update this object.")
