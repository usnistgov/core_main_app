""" Common Validators
"""
import os
import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext


@deconstructible
class BlankSpacesValidator:
    """BlankSpacesValidator"""

    def __call__(self, value):
        """__call__

        Args:
            value:

        Returns:

        """
        value = force_str(value)
        if len(value.strip()) == 0:
            raise ValidationError(
                _("This field should not be empty."),
            )


@deconstructible
class ExtensionValidator:
    """ExtensionValidator"""

    def __init__(self, valid_extensions=None):
        """__init__

        Args:
            valid_extensions:
        """
        self.valid_extensions = valid_extensions if valid_extensions else []

    def __call__(self, value):
        """__call__

        Args:
            value:

        Returns:

        """
        ext = os.path.splitext(value.name)[1]
        if not ext.lower() in self.valid_extensions:
            raise ValidationError(
                _("Unsupported file extension."),
            )


class UpperCaseLetterCountValidator:
    """Counts the occurrences of uppercase letters and raises a :class:`~django.core.exceptions.ValidationError` if the count
    is less than :func:`~UpperCaseLetterCountValidator.get_min_count`.
    """

    def __init__(self, min_uppercase_letters=0):
        """__init__

        Args:
            min_uppercase_letters:
        """
        self.min_uppercase_letters = min_uppercase_letters

    def validate(self, password, user=None):
        """validate

        Args:
            password:
            user:

        Returns:

        """
        if (
            sum(1 for char in password if char.isupper())
            < self.get_min_count()
        ):
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        """Returns this validator's error message."""
        msg = (
            ngettext(
                "Your password must contain %d or more uppercase letter.",
                "Your password must contain %d or more uppercase letters.",
                self.get_min_count(),
            )
            % self.get_min_count()
        )
        return msg

    def get_min_count(self):
        """Returns: Min uppercase letters"""
        return self.min_uppercase_letters


class LowerCaseLetterCountValidator:
    """Counts the occurrences of lowercase letters and raises
    a :class:`~django.core.exceptions.ValidationError`
    if the count is less than :func:`~LowerCaseLetterCountValidator.get_min_count`.
    """

    def __init__(self, min_lowercase_letters=0):
        """__init__

        Args:
            min_lowercase_letters:
        """
        self.min_lowercase_letters = min_lowercase_letters

    def validate(self, password, user=None):
        """validate

        Args:
            password:
            user:

        Returns:

        """
        if (
            sum(1 for char in password if char.islower())
            < self.get_min_count()
        ):
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        """Returns this validator's error message."""
        msg = (
            ngettext(
                "Your password must contain %d or more lowercase letter.",
                "Your password must contain %d or more lowercase letters.",
                self.get_min_count(),
            )
            % self.get_min_count()
        )
        return msg

    def get_min_count(self):
        """Returns: Min lowercase letters"""
        return self.min_lowercase_letters


class AlphabeticCharCountValidator:
    """Counts the occurrences of letters and raises
    a :class:`~django.core.exceptions.ValidationError` if the count
    is less than :func:`~AlphabeticCharCountValidator.get_min_count`.
    """

    def __init__(self, min_alphabetic_letters=0):
        """__init__

        Args:
            min_alphabetic_letters:
        """
        self.min_alphabetic_letters = min_alphabetic_letters

    def validate(self, password, user=None):
        """validate

        Args:
            password:
            user:

        Returns:

        """
        if (
            sum(1 for char in password if self.is_alpha(char))
            < self.get_min_count()
        ):
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        """Returns this validator's error message."""
        msg = (
            ngettext(
                "Your password must contain %d or more alphabetic letter.",
                "Your password must contain %d or more alphabetic letters.",
                self.get_min_count(),
            )
            % self.get_min_count()
        )
        return msg

    def is_alpha(self, char):
        """is_alpha

        Args:
            char:

        Returns:

        """
        regex = r"[0-9a-zA-Z]"
        res = re.findall(regex, char)
        return len(res) > 0

    def get_min_count(self):
        """Returns: Min alphabetic letters"""
        return self.min_alphabetic_letters


class MaxOccurrenceCountValidator:
    """Counts the occurrences of same letters and raises
    a :class:`~django.core.exceptions.ValidationError` if the count
    is more than :func:`~MaxOccurrenceCountValidator.get_min_count`.
    """

    def __init__(self, max_occurrence=0):
        """__init__

        Args:
            max_occurrence:
        """
        self.max_occurrence = max_occurrence

    def validate(self, password, user=None):
        """validate

        Args:
            password:
            user:

        Returns:

        """
        if self.max_occurrence > 0:
            for current_char in password:
                if (
                    sum(1 for char in password if char == current_char)
                    >= self.get_max_count()
                ):
                    raise ValidationError(self.get_help_text())

    def get_help_text(self):
        """Returns this validator's error message."""
        msg = (
            ngettext(
                "Your password must contain less than %d occurrences of the same letter.",
                "Your password must contain less than %d occurrences of the same letter.",
                self.get_max_count(),
            )
            % self.get_max_count()
        )
        return msg

    def get_max_count(self):
        """Returns: Max occurrence"""
        return self.max_occurrence


class NonAlphanumericCountValidator:
    """Counts the occurrences of Non-Alphanumeric and raises
    a :class:`~django.core.exceptions.ValidationError` if the count
    is less than :func:`~NonAlphanumericCountValidator.get_min_count`.
    """

    regex = r"[^0-9a-zA-Z]"

    def __init__(self, min_nonalphanumeric_letters=0):
        """__init__

        Args:
            min_nonalphanumeric_letters:
        """
        self.min_nonalphanumeric_letters = min_nonalphanumeric_letters

    def validate(self, password, user=None):
        """validate

        Args:
            password:
            user:

        Returns:

        """
        res = re.findall(self.regex, password)
        if len(res) < self.get_min_count():
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        """Returns this validator's error message."""
        msg = (
            ngettext(
                "Your password must contain %d or more Non-Alphanumeric character.",
                "Your password must contain %d or more Non-Alphanumeric characters.",
                self.get_min_count(),
            )
            % self.get_min_count()
        )
        return msg

    def get_min_count(self):
        """Returns: Min Non-Alphanumeric letters"""
        return self.min_nonalphanumeric_letters


class DigitsCountValidator:
    """Counts the occurrences of digits and raises
    a :class:`~django.core.exceptions.ValidationError` if the count
    is less than :func:`~DigitsCountValidator.get_min_count`.
    """

    regex = r"[0-9]"

    def __init__(self, min_digits=0):
        """__init__

        Args:
            min_digits:
        """
        self.min_digits = min_digits

    def validate(self, password, user=None):
        """validate

        Args:
            password:
            user:

        Returns:

        """
        res = re.findall(self.regex, password)
        if len(res) < self.get_min_count():
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        """Returns this validator's error message."""
        msg = (
            ngettext(
                "Your password must contain %d or more digit.",
                "Your password must contain %d or more digits.",
                self.get_min_count(),
            )
            % self.get_min_count()
        )
        return msg

    def get_min_count(self):
        """Returns: Min Non-Alphanumeric letters"""
        return self.min_digits
