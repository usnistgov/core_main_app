""" Common Validators
"""
import os
import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.contrib.auth.password_validation import MinimumLengthValidator, \
    UserAttributeSimilarityValidator, CommonPasswordValidator

from core_main_app.settings import PASSWORD_MIN_LENGTH, PASSWORD_MIN_UPPERCASE_LETTERS, PASSWORD_MIN_LOWERCASE_LETTERS, \
    PASSWORD_MIN_NUMBERS, PASSWORD_MIN_SYMBOLS, PASSWORD_MIN_LETTERS, PASSWORD_MAX_OCCURRENCE


@deconstructible
class BlankSpacesValidator(object):
    def __call__(self, value):
        value = force_text(value)
        if len(value.strip()) == 0:
            raise ValidationError(
                _('This field should not be empty.'),
            )


@deconstructible
class ExtensionValidator(object):
    def __init__(self, valid_extensions=list()):
        self.valid_extensions = valid_extensions

    def __call__(self, value):
        ext = os.path.splitext(value.name)[1]
        if not ext.lower() in self.valid_extensions:
            raise ValidationError(
                _('Unsupported file extension.'),
            )


class UpperCaseLetterCountValidator(object):
    """ Counts the occurrences of uppercase letters and raises a :class:`~django.core.exceptions.ValidationError` if the count
    is less than :func:`~UpperCaseLetterCountValidator.get_min_count`.
    """

    def __init__(self, min_uppercase_letters=0):
        self.min_uppercase_letters = min_uppercase_letters

    def validate(self, password, user=None):
        if sum(1 for char in password if char.isupper()) < self.get_min_count():
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        """ Returns this validator's error message.
        """
        msg = ungettext("The new password must contain %d or more uppercase letter.",
                        "The new password must contain %d or more uppercase letters.",
                        self.get_min_count()) % self.get_min_count()
        return msg

    def get_min_count(self):
        """ Returns: Min uppercase letters
        """
        return self.min_uppercase_letters


class LowerCaseLetterCountValidator(object):
    """ Counts the occurrences of lowercase letters and raises a :class:`~django.core.exceptions.ValidationError` if the count
    is less than :func:`~LowerCaseLetterCountValidator.get_min_count`.
    """

    def __init__(self, min_lowercase_letters=0):
        self.min_lowercase_letters = min_lowercase_letters

    def validate(self, password, user=None):
        if sum(1 for char in password if char.islower()) < self.get_min_count():
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        """ Returns this validator's error message.
        """
        msg = ungettext("The new password must contain %d or more lowercase letter.",
                        "The new password must contain %d or more lowercase letters.",
                        self.get_min_count()) % self.get_min_count()
        return msg

    def get_min_count(self):
        """ Returns: Min lowercase letters
        """
        return self.min_lowercase_letters


class AlphabeticCharCountValidator(object):
    """ Counts the occurrences of letters and raises a :class:`~django.core.exceptions.ValidationError` if the count
    is less than :func:`~AlphabeticCharCountValidator.get_min_count`.
    """

    def __init__(self, min_alphabetic_letters=0):
        self.min_alphabetic_letters = min_alphabetic_letters

    def validate(self, password, user=None):
        if sum(1 for char in password if self.is_alpha(char)) < self.get_min_count():
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        """ Returns this validator's error message.
        """
        msg = ungettext("The new password must contain %d or more alphabetic letter.",
                        "The new password must contain %d or more alphabetic letters.",
                        self.get_min_count()) % self.get_min_count()
        return msg

    def is_alpha(self, char):
        regex = r"[0-9a-zA-Z]"
        res = re.findall(regex, char)
        return len(res) > 0

    def get_min_count(self):
        """ Returns: Min alphabetic letters
        """
        return self.min_alphabetic_letters


class MaxOccurrenceCountValidator(object):
    """ Counts the occurrences of same letters and raises a :class:`~django.core.exceptions.ValidationError` if the count
    is more than :func:`~MaxOccurrenceCountValidator.get_min_count`.
    """

    def __init__(self, max_occurrence=None):
        self.max_occurrence = max_occurrence

    def validate(self, password, user=None):
        if self.max_occurrence and self.max_occurrence > 0:
            for current_char in password:
                if sum(1 for char in password if char == current_char) >= self.get_max_count():
                    raise ValidationError(self.get_help_text())

    def get_help_text(self):
        """ Returns this validator's error message.
        """
        msg = ungettext("The new password must contain less than %d time the same letter.",
                        "The new password must contain less than %d times the same letter.",
                        self.get_max_count()) % self.get_max_count()
        return msg

    def get_max_count(self):
        """ Returns: Max occurrence
        """
        return self.max_occurrence


class NonAlphanumericCountValidator(object):
    """ Counts the occurrences of Non-Alphanumeric and raises a :class:`~django.core.exceptions.ValidationError` if the count
    is less than :func:`~NonAlphanumericCountValidator.get_min_count`.
    """
    regex = r"[^0-9a-zA-Z]"

    def __init__(self, min_nonalphanumeric_letters=0):
        self.min_nonalphanumeric_letters = min_nonalphanumeric_letters

    def validate(self, password, user=None):
        res = re.findall(self.regex, password)
        if len(res) < self.get_min_count():
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        """ Returns this validator's error message.
        """
        msg = ungettext("The new password must contain %d or more Non-Alphanumeric letter.",
                        "The new password must contain %d or more Non-Alphanumeric letters.",
                        self.get_min_count()) % self.get_min_count()
        return msg

    def get_min_count(self):
        """ Returns: Min Non-Alphanumeric letters
        """
        return self.min_nonalphanumeric_letters


class DigitsCountValidator(object):
    """ Counts the occurrences of digits and raises a :class:`~django.core.exceptions.ValidationError` if the count
    is less than :func:`~DigitsCountValidator.get_min_count`.
    """
    regex = r"[0-9]"

    def __init__(self, min_digits_letters=0):
        self.min_digits_letters = min_digits_letters

    def validate(self, password, user=None):
        res = re.findall(self.regex, password)
        if len(res) < self.get_min_count():
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        """ Returns this validator's error message.
        """
        msg = ungettext("The new password must contain %d or more digits.",
                        "The new password must contain %d or more digit.",
                        self.get_min_count()) % self.get_min_count()
        return msg

    def get_min_count(self):
        """ Returns: Min Non-Alphanumeric letters
        """
        return self.min_digits_letters


def validate_password(password):
    """ Validate the given password, throw a ValidationError if at least on validator fail
    :param password:
    :return:
    """
    django_validate_password(password, password_validators=
    [MinimumLengthValidator(min_length=PASSWORD_MIN_LENGTH),
     UserAttributeSimilarityValidator(),
     CommonPasswordValidator(),
     UpperCaseLetterCountValidator(min_uppercase_letters=PASSWORD_MIN_UPPERCASE_LETTERS),
     LowerCaseLetterCountValidator(min_lowercase_letters=PASSWORD_MIN_LOWERCASE_LETTERS),
     NonAlphanumericCountValidator(min_nonalphanumeric_letters=PASSWORD_MIN_SYMBOLS),
     AlphabeticCharCountValidator(min_alphabetic_letters=PASSWORD_MIN_LETTERS),
     DigitsCountValidator(min_digits_letters=PASSWORD_MIN_NUMBERS),
     MaxOccurrenceCountValidator(
         max_occurrence=PASSWORD_MAX_OCCURRENCE)])