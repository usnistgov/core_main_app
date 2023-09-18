""" Unit Test JSON utils
"""
import json
from unittest.case import TestCase

from jsonschema.validators import Draft7Validator

from core_main_app.commons.exceptions import JSONError
from core_main_app.utils.json_utils import (
    is_schema_valid,
    validate_json_data,
    _get_json_validator,
    DEFAULT_VALIDATOR,
    format_content_json,
    is_well_formed_json,
)


class TestIsSchemaValid(TestCase):
    """TestIsSchemaValid"""

    def test_is_schema_valid_with_valid_schema_does_not_raise_error(self):
        """test_is_schema_valid_with_valid_schema_does_not_raise_error"""
        is_schema_valid(get_json_schema())

    def test_is_schema_valid_with_valid_str_schema_does_not_raise_error(self):
        """test_is_schema_valid_with_valid_str_schema_does_not_raise_error"""
        is_schema_valid(json.dumps(get_json_schema()))

    def test_is_schema_valid_with_invalid_schema_raises_json_error(self):
        """test_is_schema_valid_with_invalid_schema_raises_json_error"""
        json_schema = {"bad"}
        with self.assertRaises(JSONError):
            is_schema_valid(json_schema)


class TestGetJsonValidator(TestCase):
    """TestGetJsonValidator"""

    def test_get_json_validator_returns_default_validator_if_no_schema_specified(
        self,
    ):
        """test_get_json_validator_returns_default_validator_if_no_schema_specified"""
        json_validator = _get_json_validator({})
        self.assertEqual(json_validator, DEFAULT_VALIDATOR)

    def test_get_json_validator_returns_default_validator_if_unknown_schema_specified(
        self,
    ):
        """test_get_json_validator_returns_default_validator_if_unknown_schema_specified"""
        json_validator = _get_json_validator({"$schema": "test"})
        self.assertEqual(json_validator, DEFAULT_VALIDATOR)

    def test_get_json_validator_returns_validator_if_schema_specified(self):
        """test_get_json_validator_returns_validator_if_schema_specified"""
        json_validator = _get_json_validator(get_json_schema())
        self.assertEqual(json_validator, Draft7Validator)


class TestValidateJsonData(TestCase):
    """TestValidateJsonData"""

    def test_validate_json_data_with_valid_data(self):
        """test_validate_json_data_with_valid_data"""
        validate_json_data(get_json_data(), get_json_schema())

    def test_validate_json_data_with_invalid_data(self):
        """test_validate_json_data_with_invalid_data"""
        json_data = get_json_data()
        json_data["age"] = "Test"
        with self.assertRaises(JSONError):
            validate_json_data(json_data, get_json_schema())


class TestFormatContentJson(TestCase):
    """TestFormatContentJson"""

    def test_format_content_json_with_dict_return_formatted_dict(self):
        """test_format_content_json_with_dict_return_formatted_dict"""
        json_dict = {"test": "value"}
        expected_result = """{\n  "test": "value"\n}"""
        result = format_content_json(json_dict, indent=2)
        self.assertEqual(result, expected_result)

    def test_format_content_json_with_str_return_formatted_dict(self):
        """test_format_content_json_with_str_return_formatted_dict"""
        json_str = '{"test": "value"}'
        expected_result = """{\n  "test": "value"\n}"""
        result = format_content_json(json_str, indent=2)
        self.assertEqual(result, expected_result)

    def test_format_content_json_with_invalid_format_return_formatted_dict(
        self,
    ):
        """test_format_content_json_with_invalid_format_return_formatted_dict"""
        invalid_format = 10
        with self.assertRaises(JSONError):
            format_content_json(invalid_format)

    def test_format_content_json_with_invalid_str_return_formatted_dict(self):
        """test_format_content_json_with_invalid_str_return_formatted_dict"""
        invalid_json_str = '{"test":}'
        with self.assertRaises(JSONError):
            format_content_json(invalid_json_str)


class TestIsWellFormedContentJson(TestCase):
    """TestIsWellFormedContentJson"""

    def test_is_content_json_well_formed_with_dict_returns_true(self):
        """test_is_content_json_well_formed_returns_true"""
        json_dict = {"test": "value"}
        expected_result = True
        result = is_well_formed_json(json_dict)
        self.assertEqual(result, expected_result)

    def test_is_content_json_well_formed_with_str_returns_true(self):
        """test_is_content_json_well_formed_returns_true"""
        json_str = '{"test": "value"}'
        expected_result = True
        result = is_well_formed_json(json_str)
        self.assertEqual(result, expected_result)

    def test_is_content_json_well_formed_invalid_format_returns_false(self):
        """test_is_content_json_well_formed_invalid_format_returns_false"""
        json_dict = 10
        expected_result = False
        result = is_well_formed_json(json_dict)
        self.assertEqual(result, expected_result)

    def test_is_content_json_well_formed_invalid_str_returns_false(self):
        """test_is_content_json_well_formed_invalid_str_returns_false"""
        json_dict = "sda"
        expected_result = False
        result = is_well_formed_json(json_dict)
        self.assertEqual(result, expected_result)


def get_json_schema():
    """Return JSON schema

    Returns:

    """
    return {
        "$id": "https://example.com/person.schema.json",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Person",
        "type": "object",
        "properties": {
            "firstName": {
                "type": "string",
                "description": "The person's first name.",
            },
            "lastName": {
                "type": "string",
                "description": "The person's last name.",
            },
            "age": {
                "description": "Age in years which must be equal to or greater than zero.",
                "type": "integer",
                "minimum": 0,
            },
        },
    }


def get_json_data():
    """Return valid JSON data

    Args:

    Returns:

    """
    return {"firstName": "John", "lastName": "Doe", "age": 21}
