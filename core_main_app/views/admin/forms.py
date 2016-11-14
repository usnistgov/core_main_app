from django import forms


class UploadTemplateForm(forms.Form):
    """
    Form to upload a new Template
    """
    name = forms.CharField(label='Enter Template name', max_length=100, required=True)
    xsd_file = forms.FileField(label='Select a file', required=True)
