""" Labels utils
"""
from django.utils.translation import ugettext as _


def get_data_label():
    """Get the correct label for a record/resource.

    Returns:
    """
    return _("record_label")


def get_form_label():
    """Get the correct label for a form/draft.

    Returns:
    """
    return _("form_label")
