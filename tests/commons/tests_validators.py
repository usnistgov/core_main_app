""" Unit Test Validators
"""
import unittest

from django.core.exceptions import ValidationError

from core_main_app.commons.validators import (
    UpperCaseLetterCountValidator,
    LowerCaseLetterCountValidator,
    AlphabeticCharCountValidator,
    MaxOccurrenceCountValidator,
    NonAlphanumericCountValidator,
    DigitsCountValidator,
    BlankSpacesValidator,
)


class TestValidators(unittest.TestCase):
    """Test Validators"""

    def test_blank_spaces_validator_should_pass(self):
        """Test blank spaces case validator should pass

        Returns:

        """
        blank_spaces_validator = BlankSpacesValidator()
        blank_spaces_validator("PasswordTest")

    def test_blank_spaces_validator_should_fail(self):
        """Test blank spaces case validator should fail

        Returns:

        """
        blank_spaces_validator = BlankSpacesValidator()
        with self.assertRaises(ValidationError):
            blank_spaces_validator(" ")

    def test_upper_case_validator_should_pass(self):
        """Test upper case validator should pass

        Returns:

        """
        uppercase_validator = UpperCaseLetterCountValidator(2)
        uppercase_validator.validate("passWordTest")

    def test_upper_case_validator_should_fail(self):
        """Test upper case validator should fail

        Returns:

        """
        uppercase_validator = UpperCaseLetterCountValidator(2)
        with self.assertRaises(ValidationError):
            uppercase_validator.validate("passwordtest")

    def test_lower_case_validator_should_pass(self):
        """Test lower case validator should pass

        Returns:

        """
        lowercase_validator = LowerCaseLetterCountValidator(2)
        lowercase_validator.validate("PaSSWoRDTeST")

    def test_lower_case_validator_should_fail(self):
        """Test lower case validator should fail

        Returns:

        """
        lowercase_validator = LowerCaseLetterCountValidator(2)
        with self.assertRaises(ValidationError):
            lowercase_validator.validate("PASSWORDTEST")

    def test_alphabetic_validator_should_pass(self):
        """Test alphabetic validator should pass

        Returns:

        """
        alpha_validator = AlphabeticCharCountValidator(5)
        alpha_validator.validate("!@#$t%^&j&*(y(*%t$#@A*")

    def test_alphabetic_validator_should_fail(self):
        """Test alphabetic validator should fail

        Returns:

        """
        alpha_validator = AlphabeticCharCountValidator(2)
        with self.assertRaises(ValidationError):
            alpha_validator.validate("!@#$%^&&*((*%$#@*")

    def test_max_occurrence_validator_should_pass(self):
        """Test max occurrence validator should pass

        Returns:

        """
        max_occur_validator = MaxOccurrenceCountValidator(5)
        max_occur_validator.validate("abbcccdddd")

    def test_max_occurrence_validator_should_fail(self):
        """Test max occurrence validator should fail

        Returns:

        """
        max_occur_validator = MaxOccurrenceCountValidator(2)
        with self.assertRaises(ValidationError):
            max_occur_validator.validate("abbcccddddeeeee")

    def test_non_alphanumeric_validator_should_pass(self):
        """Test non alphanumeric validator should pass

        Returns:

        """
        non_alphanumeric_validator = NonAlphanumericCountValidator(5)
        non_alphanumeric_validator.validate("abbccc!@dddd$%eeee*")

    def test_non_alphanumeric_validator_should_fail(self):
        """Test non alphanumeric validator should fail

        Returns:

        """
        non_alphanumeric_validator = NonAlphanumericCountValidator(5)
        with self.assertRaises(ValidationError):
            non_alphanumeric_validator.validate("abbc*ccdd@ddee#eee")

    def test_digits_validator_should_pass(self):
        """Test digit validator should pass

        Returns:

        """
        digits_validator = DigitsCountValidator(5)
        digits_validator.validate("abbccc12345dddd")

    def test_digits_validator_should_fail(self):
        """Test digit validator should fail

        Returns:

        """
        digits_validator = DigitsCountValidator(5)
        with self.assertRaises(ValidationError):
            digits_validator.validate("abbccc1234dddd")
