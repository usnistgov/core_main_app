""" Utils for template version manager rest Apis
"""
import json

from core_main_app.commons.exceptions import RestApiError


def load_dependencies(validated_data):
    """Return dependencies as a dict.

    Args:
        validated_data:

    Returns:

    """
    if "dependencies_dict" in validated_data:
        dependencies_dict = validated_data["dependencies_dict"]
        try:
            return json.loads(dependencies_dict)
        except Exception:
            raise RestApiError(
                "Incorrect format of the dependencies parameter."
            )
    return None
