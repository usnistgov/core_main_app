""" Forms
"""

from django import forms

from core_main_app.commons.validators import BlankSpacesValidator


class UploadForm(forms.Form):
    """
    Form to upload.
    """

    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[BlankSpacesValidator()],
    )
    upload_file = forms.FileField(label="Select a file", required=True)
