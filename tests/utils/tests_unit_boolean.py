""" Boolean utils test class
"""
from unittest import TestCase

from core_main_app.utils.boolean import to_bool


class TestToBool(TestCase):
    """Test to_bool"""

    def test_boolean_false_expected_case_returns_false(self):
        """test boolean false expected case returns false

        Returns:

        """
        self.assertEqual(to_bool("False"), False)

    def test_boolean_true_expected_case_returns_true(self):
        """test boolean true expected case returns true

        Returns:

        """
        self.assertEqual(to_bool("True"), True)

    def test_boolean_false_unexpected_case_returns_false(self):
        """test boolean false unexpected case returns false

        Returns:

        """
        self.assertEqual(to_bool("false"), False)

    def test_boolean_true_unexpected_case_returns_true(self):
        """test boolean true unexpected case returns true

        Returns:

        """
        self.assertEqual(to_bool("true"), True)

    def test_boolean_false_returns_false(self):
        """test boolean false returns false

        Returns:

        """
        self.assertEqual(to_bool(False), False)

    def test_boolean_true_returns_true(self):
        """test boolean true returns true

        Returns:

        """
        self.assertEqual(to_bool(True), True)

    def test_unexpected_string_raises_value_error(self):
        """test unexpected string raises value error

        Returns:

        """
        with self.assertRaises(ValueError):
            to_bool("bool")

    def test_unexpected_type_raises_value_error(self):
        """test unexpected type raises value error

        Returns:

        """
        with self.assertRaises(ValueError):
            to_bool(1)
