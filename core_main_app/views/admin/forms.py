"""Forms for admin views
"""
from django import forms

from core_main_app.commons.validators import ExtensionValidator
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager.models import TemplateVersionManager
from core_main_app.components.xsl_transformation import api as xsl_transformation_api
from core_main_app.components.xsl_transformation.models import XslTransformation
from core_main_app.views.admin.commons.upload.forms import UploadForm
from django_mongoengine.forms import DocumentForm


class EditTemplateForm(DocumentForm):
    title = forms.CharField(label='Name',
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Type the new name'}))

    class Meta(object):
        document = TemplateVersionManager
        fields = ['title']


class EditXSLTForm(DocumentForm):
    name = forms.CharField(label='Name',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Type the new name'}))

    class Meta(object):
        document = XslTransformation
        fields = ['name']


class UploadTemplateForm(UploadForm):
    """
    Form to upload a new Template
    """

    def __init__(self, *args, **kwargs):
        super(UploadTemplateForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Enter Template name'
        self.fields['upload_file'].widget = forms.FileInput(attrs={'accept': '.xsd'})


class UploadVersionForm(forms.Form):
    """
    Form to upload a new version
    """
    xsd_file = forms.FileField(label='Select a file', required=True,
                               widget=forms.FileInput(attrs={'accept': '.xsd'}))


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
        self.fields['upload_file'].validators = [ExtensionValidator('.xsl')]
        self.fields['upload_file'].widget = forms.FileInput(attrs={'accept': '.xslt, .xsl'})


class TemplateXsltRenderingForm(forms.Form):
    """
    Form to associate list and detail XSLTs to template
    """
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    template = forms.ModelChoiceField(widget=forms.HiddenInput(), required=False, queryset=template_api.get_all())
    list_xslt = forms.ModelChoiceField(label='List XSLT', empty_label="(No XSLT)", required=False,
                                       widget=forms.Select(attrs={'class': 'form-control'}),
                                       queryset=xsl_transformation_api.get_all())
    detail_xslt = forms.ModelChoiceField(label='Detail XSLT', empty_label="(No XSLT)", required=False,
                                         widget=forms.Select(attrs={'class': 'form-control'}),
                                         queryset=xsl_transformation_api.get_all())


class TextAreaForm(forms.Form):
    """ TextArea Form
    """
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control'}),
                              required=False)
