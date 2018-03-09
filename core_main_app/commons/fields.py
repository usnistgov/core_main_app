""" Common custom fields
"""
from django import forms
from core_main_app import settings
from password_policies.forms.fields import PasswordPoliciesField
from core_main_app.commons.validators import UpperCaseLetterCountValidator, LowerCaseLetterCountValidator


class CustomPasswordPoliciesField(PasswordPoliciesField):
    """ A form field that validates a password using :doc:`validators`.
    """

    def __init__(self, *args, **kwargs):
        if "widget" not in kwargs:
            kwargs["widget"] = forms.PasswordInput(render_value=False)
        kwargs["min_length"] = settings.PASSWORD_MIN_LENGTH
        self.default_validators.append(UpperCaseLetterCountValidator(settings.PASSWORD_MIN_UPPERCASE_LETTERS))
        self.default_validators.append(LowerCaseLetterCountValidator(settings.PASSWORD_MIN_LOWERCASE_LETTERS))
        super(CustomPasswordPoliciesField, self).__init__(*args, **kwargs)
