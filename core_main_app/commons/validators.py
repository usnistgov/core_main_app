""" Common Validators
"""
from django.utils.translation import ungettext
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text
from password_policies.forms.validators import BaseCountValidator
import os


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


class UpperCaseLetterCountValidator(BaseCountValidator):
    """ Counts the occurrences of letters and raises a :class:`~django.core.exceptions.ValidationError` if the count
    is less than :func:`~UpperCaseLetterCountValidator.get_min_count`.
    """
    categories = ['Lu']
    """ The unicode data letter categories:

    ====  ===========
    Code  Description
    ====  ===========
    LC    Letter, Cased
    Ll    Letter, Lowercase
    Lu    Letter, Uppercase
    Lt    Letter, Titlecase
    Lo    Letter, Other
    Nl    Number, Letter
    ====  ===========
    """
    #: The validator's error code.
    code = u"invalid_letter_count"

    def __init__(self, min_uppercase_letters):
        self.min_uppercase_letters = min_uppercase_letters

    def get_error_message(self):
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


class LowerCaseLetterCountValidator(BaseCountValidator):
    """ Counts the occurrences of letters and raises a :class:`~django.core.exceptions.ValidationError` if the count
    is less than :func:`~LowerCaseLetterCountValidator.get_min_count`.
    """
    categories = ['Ll']
    """
    The unicode data letter categories:
    ====  ===========
    Code  Description
    ====  ===========
    LC    Letter, Cased
    Ll    Letter, Lowercase
    Lu    Letter, Uppercase
    Lt    Letter, Titlecase
    Lo    Letter, Other
    Nl    Number, Letter
    ====  ===========
    """
    #: The validator's error code.
    code = u"invalid_letter_count"

    def __init__(self, min_lowercase_letters):
        self.min_lowercase_letters = min_lowercase_letters

    def get_error_message(self):
        """ Returns this validator's error message.
        """
        msg = ungettext("The new password must contain %d or more lower letter.",
                        "The new password must contain %d or more lower letters.",
                        self.get_min_count()) % self.get_min_count()
        return msg

    def get_min_count(self):
        """ Returns: Min lowercase letters
        """
        return self.min_lowercase_letters
