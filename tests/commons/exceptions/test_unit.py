""" Unit tests for `core_main_app.commons.exceptions` package.
"""
from unittest import TestCase
from core_main_app.commons.exceptions import JSONError


class TestJSONErrorInit(TestCase):
    """Unit tests for `JSONError.__init__` method."""

    def test_init_with_list(self):
        """test_init_with_list"""
        json_error_input = ["error1", "error2"]
        json_error = JSONError(json_error_input)

        self.assertEqual(json_error.message_list, json_error_input)

    def test_init_with_str(self):
        """test_init_with_str"""
        json_error_input = "error1"
        json_error = JSONError(json_error_input)

        self.assertEqual(json_error.message_list, [json_error_input])

    def test_init_with_other(self):
        """test_init_with_other"""
        json_error_input = Exception("mock_exception")
        json_error = JSONError(json_error_input)

        self.assertEqual(json_error.message_list, [str(json_error_input)])


class TestJSONErrorStr(TestCase):
    """Unit tests for `JSONError.__str_` method."""

    def test_print_list_succesful(self):
        json_error_input = ["error1", "error2"]
        json_error = JSONError(json_error_input)

        self.assertEqual(str(json_error), ", ".join(json_error_input))
