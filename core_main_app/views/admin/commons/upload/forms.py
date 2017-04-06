from django import forms


class UploadForm(forms.Form):
    """
    Form to upload.
    """
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    upload_file = forms.FileField(label='Select a file', required=True)
