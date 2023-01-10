""" Validate filename test case
"""
from unittest import TestCase

from django.core.exceptions import ValidationError

from core_main_app.utils.validation.regex_validation import validate_filename


class TestValidateFilename(TestCase):
    """Test validate_filename"""

    def test_validate_filename_ok_if_filename_ok(self):
        """test_validate_filename_ok_if_filename_ok

        Returns:

        """
        validate_filename("test.png")

    def test_validate_filename_if_extension_missing(self):
        """test_validate_filename_if_extension_missing

        Returns:

        """
        with self.assertRaises(ValidationError):
            validate_filename("test")
