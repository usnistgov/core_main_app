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
)


class TestValidators(unittest.TestCase):
    def test_upper_case_validator_should_pass(self):

        try:
            uppercase_validator = UpperCaseLetterCountValidator(2)
            uppercase_validator.validate("passWordTest")
        except ValidationError as validation_error:
            self.fail("The validator should not raise a ValidationError.")
        except Exception as ex:
            self.fail("The validator should not raise an Exception.")

    def test_upper_case_validator_should_fail(self):
        uppercase_validator = UpperCaseLetterCountValidator(2)
        with self.assertRaises(ValidationError):
            uppercase_validator.validate("passwordtest")

    def test_lower_case_validator_should_pass(self):

        try:
            lowercase_validator = LowerCaseLetterCountValidator(2)
            lowercase_validator.validate("PaSSWoRDTeST")
        except ValidationError as validation_error:
            self.fail("The validator should not raise a ValidationError.")
        except Exception as ex:
            self.fail("The validator should not raise an Exception.")

    def test_lower_case_validator_should_fail(self):
        lowercase_validator = LowerCaseLetterCountValidator(2)
        with self.assertRaises(ValidationError):
            lowercase_validator.validate("PASSWORDTEST")

    def test_alphabetic_validator_should_pass(self):

        try:
            alpha_validator = AlphabeticCharCountValidator(5)
            alpha_validator.validate("!@#$t%^&j&*(y(*%t$#@A*")
        except ValidationError as validation_error:
            self.fail("The validator should not raise a ValidationError.")
        except Exception as ex:
            self.fail("The validator should not raise an Exception.")

    def test_alphabetic_validator_should_fail(self):
        alpha_validator = AlphabeticCharCountValidator(2)
        with self.assertRaises(ValidationError):
            alpha_validator.validate("!@#$%^&&*((*%$#@*")

    def test_max_occurrence_validator_should_pass(self):

        try:
            max_occur_validator = MaxOccurrenceCountValidator(5)
            max_occur_validator.validate("abbcccdddd")
        except ValidationError as validation_error:
            self.fail("The validator should not raise a ValidationError.")
        except Exception as ex:
            self.fail("The validator should not raise an Exception.")

    def test_max_occurrence_validator_should_fail(self):
        max_occur_validator = MaxOccurrenceCountValidator(2)
        with self.assertRaises(ValidationError):
            max_occur_validator.validate("abbcccddddeeeee")

    def test_non_alphanumeric_validator_should_pass(self):

        try:
            non_alphanumeric_validator = NonAlphanumericCountValidator(5)
            non_alphanumeric_validator.validate("abbccc!@dddd$%eeee*")
        except ValidationError as validation_error:
            self.fail("The validator should not raise a ValidationError.")
        except Exception as ex:
            self.fail("The validator should not raise an Exception.")

    def test_non_alphanumeric_validator_should_fail(self):
        non_alphanumeric_validator = NonAlphanumericCountValidator(5)
        with self.assertRaises(ValidationError):
            non_alphanumeric_validator.validate("abbc*ccdd@ddee#eee")

    def test_digits_validator_should_pass(self):

        try:
            digits_validator = DigitsCountValidator(5)
            digits_validator.validate("abbccc12345dddd")
        except ValidationError as validation_error:
            self.fail("The validator should not raise a ValidationError.")
        except Exception as ex:
            self.fail("The validator should not raise an Exception.")

    def test_digits_validator_should_fail(self):
        digits_validator = DigitsCountValidator(5)
        with self.assertRaises(ValidationError):
            digits_validator.validate("abbccc1234dddd")
