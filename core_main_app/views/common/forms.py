""" Common forms
"""
from django import forms

from core_main_app.commons.validators import BlankSpacesValidator


class RenameForm(forms.Form):
    """Rename form"""

    field = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Type the new name"}
        ),
        validators=[BlankSpacesValidator()],
    )

    id = forms.CharField(widget=forms.HiddenInput(), required=False)
