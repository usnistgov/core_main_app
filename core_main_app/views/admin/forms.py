"""Forms for admin views
"""
from django import forms
from django.conf import settings
from django.forms import ModelForm

from core_main_app.commons.constants import (
    TEMPLATE_FILE_EXTENSION_FOR_TEMPLATE_FORMAT,
)
from core_main_app.commons.validators import ExtensionValidator
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.components.xsl_transformation import (
    api as xsl_transformation_api,
)
from core_main_app.components.xsl_transformation.models import (
    XslTransformation,
)
from core_main_app.views.admin.commons.upload.forms import UploadForm


class EditTemplateForm(ModelForm):
    """Edit Template Form"""

    title = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Type the new name"}
        ),
    )

    class Meta:
        """Meta"""

        model = TemplateVersionManager
        fields = ["title"]


class EditXSLTForm(ModelForm):
    """Edit XSLT Form"""

    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Type the new name"}
        ),
    )

    class Meta:
        """Meta"""

        model = XslTransformation
        fields = ["name"]


class UploadTemplateForm(UploadForm):
    """
    Form to upload a new Template
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Enter Template name"
        self.fields[
            "upload_file"
        ].help_text = (
            "JSON Schema support can be enabled in the project settings."
        )
        self.fields["upload_file"].validators = [
            ExtensionValidator(
                ",".join(TEMPLATE_FILE_EXTENSION_FOR_TEMPLATE_FORMAT.values())
            )
        ]
        self.fields["upload_file"].widget = forms.FileInput(
            attrs={
                "accept": ",".join(
                    TEMPLATE_FILE_EXTENSION_FOR_TEMPLATE_FORMAT.values()
                ),
                "class": "form-control",
            }
        )


class UploadVersionForm(forms.Form):
    """
    Form to upload a new version
    """

    xsd_file = forms.FileField(
        label="Select a file",
        required=True,
        validators=[
            ExtensionValidator(
                ",".join(TEMPLATE_FILE_EXTENSION_FOR_TEMPLATE_FORMAT.values())
            )
        ],
        widget=forms.FileInput(
            attrs={
                "accept": ",".join(
                    TEMPLATE_FILE_EXTENSION_FOR_TEMPLATE_FORMAT.values()
                )
            }
        ),
    )


class EditProfileForm(forms.Form):
    """
    Form to edit the profile information
    """

    firstname = forms.CharField(
        label="First Name", max_length=100, required=True
    )
    lastname = forms.CharField(
        label="Last Name", max_length=100, required=True
    )
    username = forms.CharField(
        label="Username",
        max_length=100,
        required=True,
        widget=forms.HiddenInput(),
    )
    email = forms.EmailField(
        label="Email Address", max_length=100, required=True
    )


class UploadXSLTForm(UploadForm):
    """
    Form to upload a new XSLT
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Enter XSLT name"
        self.fields["upload_file"].validators = [ExtensionValidator(".xsl")]
        self.fields["upload_file"].widget = forms.FileInput(
            attrs={"accept": ".xslt, .xsl"}
        )


class TemplateXsltRenderingForm(forms.Form):
    """
    Form to associate list and detail XSLTs to template
    """

    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    template = forms.CharField(widget=forms.HiddenInput(), required=False)

    list_xslt = forms.ModelChoiceField(
        label="Set XSLT to render a list of data",
        empty_label="(No XSLT)",
        required=False,
        widget=forms.Select(),
        queryset=xsl_transformation_api.get_all(),
    )

    list_detail_xslt = forms.MultipleChoiceField(
        label="Set XSLT to render a single data",
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
    )

    default_detail_xslt = forms.ModelChoiceField(
        label="Default rendering",
        empty_label="(No XSLT)",
        required=False,
        widget=forms.Select(),
        queryset=xsl_transformation_api.get_all(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["list_detail_xslt"].choices = _get_xsl_transformation()
        if settings.BOOTSTRAP_VERSION.startswith("4"):
            self.fields["list_xslt"].widget.attrs["class"] = "form-control"
            self.fields["default_detail_xslt"].widget.attrs[
                "class"
            ] = "form-control"
        elif settings.BOOTSTRAP_VERSION.startswith("5"):
            self.fields["list_xslt"].widget.attrs["class"] = "form-select"
            self.fields["default_detail_xslt"].widget.attrs[
                "class"
            ] = "form-select"


class TextAreaForm(forms.Form):
    """TextArea Form"""

    content = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=False,
    )


def _get_xsl_transformation():
    """Get XSLT.

    Returns:
        List of XSLT.

    """
    xsl_transformation = []
    list_ = xsl_transformation_api.get_all()
    for elt in list_:
        xsl_transformation.append((elt.id, elt.name))
    return xsl_transformation
