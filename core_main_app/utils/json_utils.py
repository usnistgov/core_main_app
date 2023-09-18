""" JSON utils
"""
import json

from jsonschema import validate
from jsonschema import validators as json_validators

from core_main_app.commons.exceptions import JSONError

VALIDATOR_CLASSES = {
    "https://json-schema.org/draft/2020-12/schema": json_validators.Draft202012Validator,
    "https://json-schema.org/draft/2019-09/schema": json_validators.Draft201909Validator,
    "http://json-schema.org/draft-07/schema#": json_validators.Draft7Validator,
    "http://json-schema.org/draft-06/schema#": json_validators.Draft6Validator,
    "http://json-schema.org/draft-04/schema#": json_validators.Draft4Validator,
}

DEFAULT_VALIDATOR = json_validators.Draft202012Validator


def validate_json_data(data, json_schema):
    """Validate JSON data against JSON schema

    Args:
        data: json dict
        json_schema: json schema

    Returns:

    """
    try:
        if isinstance(json_schema, str):
            json_schema = json.loads(json_schema)
        if isinstance(data, str):
            data = json.loads(data)
        validate(data, json_schema)
    except Exception as e:
        raise JSONError(str(e))


def is_schema_valid(json_schema):
    """Validate JSON schema

    Args:
        json_schema: json schema

    Returns:

    """
    if isinstance(json_schema, str):
        json_schema = json.loads(json_schema)
    json_validator = _get_json_validator(json_schema)

    try:
        json_validator.check_schema(json_schema)
    except Exception as e:
        error_message = f"Selected JSON Schema validator: {str(json_validator)}. Error: {str(e)}"
        raise JSONError(error_message)


def _get_json_validator(json_schema):
    """_get_json_validator"""
    return (
        VALIDATOR_CLASSES[json_schema["$schema"]]
        if "$schema" in json_schema
        and json_schema["$schema"] in VALIDATOR_CLASSES
        else DEFAULT_VALIDATOR
    )


def format_content_json(json_content, indent=2):
    """Format JSON content.

    Args:
        json_content:
        indent:

    Returns:

    """
    try:
        if isinstance(json_content, str):
            json_content = json.loads(json_content)
        if isinstance(json_content, dict):
            return json.dumps(json_content, indent=indent)
        raise JSONError("Invalid format.")
    except Exception:
        raise JSONError("Content is not well formatted JSON.")


def is_well_formed_json(json_content):
    """True if well formatted JSON.

    Args:
        json_content:

    Returns:

    """
    # is it a valid JSON document?
    try:
        if isinstance(json_content, str):
            json.loads(json_content)
        elif isinstance(json_content, dict):
            json.dumps(json_content)

        else:
            return False
    except Exception:
        return False

    return True
