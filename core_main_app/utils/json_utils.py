""" JSON utils
"""
import json

from jsonschema import validators as json_validators

from core_main_app.commons.exceptions import JSONError
from core_main_app.utils.dict import get_dict_keys

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
    errors = []
    try:
        if isinstance(data, str):
            data = load_json_string(data)

        if not isinstance(data, dict):  # Ensure data is a dictionary.
            errors = ["The document is not a valid JSON object"]
            return

        # Ensure the data dictionary keys do not start with '$'.
        if any(item.startswith("$") for item in get_dict_keys(data)):
            errors.append("JSON keys cannot start with '$'")

        if isinstance(json_schema, str):
            json_schema = load_json_string(json_schema)

        json_validator = _get_json_validator(json_schema)
        validation = json_validator(json_schema)

        for error in sorted(validation.iter_errors(data), key=str):
            errors.append(f"{error.json_path}: {error.message}")
    except Exception as e:
        errors = [str(e)]
    finally:  # If some errors happened, raise a JSONError.
        if len(errors) > 0:
            raise JSONError(errors)


def is_schema_valid(json_schema):
    """Validate JSON schema

    Args:
        json_schema: json schema

    Returns:

    """
    if isinstance(json_schema, str):
        json_schema = load_json_string(json_schema)
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
            json_content = load_json_string(json_content)
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
            load_json_string(json_content)
        elif isinstance(json_content, dict):
            json.dumps(json_content)

        else:
            return False
    except Exception:
        return False

    return True


def load_json_string(json_content):
    """Load a json string and checks that no duplicate keys are found.

    See https://stackoverflow.com/a/14902564/1723284

    Args:
        json_content:

    Returns:

    """

    def dict_raise_on_duplicates(ordered_pairs):
        """Reject duplicate keys."""
        json_data = {}
        for k, v in ordered_pairs:
            if k in json_data:
                raise ValueError(
                    f"Found a duplicate key '{k}' while loading the JSON"
                )
            else:
                json_data[k] = v
        return json_data

    return json.loads(json_content, object_pairs_hook=dict_raise_on_duplicates)
