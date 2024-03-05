""" Test forms.
"""
from unittest.case import TestCase

from django.test import override_settings

from core_main_app.views.admin.forms import (
    TemplateXsltRenderingForm,
    UploadTemplateForm,
)


class TestUploadTemplateForm(TestCase):
    def test_upload_form_sets_extension_validators(
        self,
    ):
        """test_upload_form_sets_extension_validators

        Returns:

        """
        form = UploadTemplateForm()
        self.assertEquals(
            form.fields["upload_file"].validators[0].valid_extensions,
            ".json,.xsd",
        )


class TestTemplateXsltRenderingForm(TestCase):
    """Test Template Xslt Rendering Form"""

    @override_settings(BOOTSTRAP_VERSION="4.6.2")
    def test_template_xslt_rendering_form_bootstrap_v4(self):
        """test_template_xslt_rendering_form_bootstrap_v4

        Returns:

        """
        data = {}
        form = TemplateXsltRenderingForm(data)
        self.assertEquals(
            form.fields["default_detail_xslt"].widget.attrs["class"],
            "form-control",
        )
        self.assertEquals(
            form.fields["list_xslt"].widget.attrs["class"], "form-control"
        )

    @override_settings(BOOTSTRAP_VERSION="5.1.3")
    def test_template_xslt_rendering_form_bootstrap_v5(self):
        """test_template_xslt_rendering_form_bootstrap_v5

        Returns:

        """
        data = {}
        form = TemplateXsltRenderingForm(data)
        self.assertEquals(
            form.fields["default_detail_xslt"].widget.attrs["class"],
            "form-select",
        )
        self.assertEquals(
            form.fields["list_xslt"].widget.attrs["class"], "form-select"
        )
