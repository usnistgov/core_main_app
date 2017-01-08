from django import forms


class UploadTemplateForm(forms.Form):
    """
    Form to upload a new Template
    """
    name = forms.CharField(label='Enter Template name', max_length=100, required=True)
    xsd_file = forms.FileField(label='Select a file', required=True)


class UploadVersionForm(forms.Form):
    """
    Form to upload a new version
    """
    xsd_file = forms.FileField(label='Select a file', required=True)


class EditProfileForm(forms.Form):
    """
    Form to edit the profile information
    """
    firstname = forms.CharField(label='First Name', max_length=100, required=True)
    lastname = forms.CharField(label='Last Name', max_length=100, required=True)
    username = forms.CharField(label='Username', max_length=100, required=True, widget=forms.HiddenInput())
    email = forms.EmailField(label='Email Address', max_length=100, required=True)