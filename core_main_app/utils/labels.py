""" Labels utils
"""
from django.conf import settings
from django.utils.translation import ugettext as _


def get_data_label():
    """ Get the correct label for a record/ressource.

    Returns:
    """
    return getattr(settings, 'DATA_DISPLAY_NAME', 'record')


def get_form_label():
    """ Get the correct label for a form/draft.

    Returns:
    """
    return _('form_label')
