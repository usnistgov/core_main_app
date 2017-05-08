from django import forms
from core_main_app.views.admin.commons.upload.forms import UploadForm
from core_main_app.components.xsl_transformation import api as xsl_transformation_api
from core_main_app.components.template import api as template_api
from core_main_app.components.template_xsl_rendering.models import TemplateXslRendering


class UploadTemplateForm(UploadForm):
    """
    Form to upload a new Template
    """
    def __init__(self, *args, **kwargs):
        super(UploadTemplateForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Enter Template name'


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


class UploadXSLTForm(UploadForm):
    """
    Form to upload a new XSLT
    """
    def __init__(self, *args, **kwargs):
        super(UploadXSLTForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Enter XSLT name'


class TemplateXsltRenderingForm(forms.Form):
    """

    """
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    template = forms.ModelChoiceField(widget=forms.HiddenInput(), required=False, queryset=template_api.get_all())
    list_xslt = forms.ModelChoiceField(label='List XSLT', empty_label="(No XSLT)", required=False,
                                       widget=forms.Select(attrs={'class': 'form-control'}),
                                       queryset=xsl_transformation_api.get_all())
    detail_xslt = forms.ModelChoiceField(label='Detail XSLT', empty_label="(No XSLT)", required=False,
                                         widget=forms.Select(attrs={'class': 'form-control'}),
                                         queryset=xsl_transformation_api.get_all())
