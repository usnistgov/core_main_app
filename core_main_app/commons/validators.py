""" Common Validators """

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text
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
    def __init__(self, valid_extensions=[]):
        self.valid_extensions = valid_extensions

    def __call__(self, value):
        ext = os.path.splitext(value.name)[1]
        if not ext.lower() in self.valid_extensions:
            raise ValidationError(
                _('Unsupported file extension.'),
            )
