""" Blob Processing Module Forms test class
"""

from unittest import TestCase

from core_main_app.components.blob_processing_module.forms import (
    BlobProcessingModuleForm,
)


class TestBlobProcessingModuleForm(TestCase):
    """TestBlobProcessingModuleForm"""

    def test_BlobProcessingModuleForm(self):
        """test_BlobProcessingModuleForm

        Returns:

        """

        form = BlobProcessingModuleForm()
        self.assertTrue("run_strategy_list" in form.fields)
        self.assertTrue("blob_filename_regexp" in form.fields)
        self.assertTrue("parameters" in form.fields)
        self.assertTrue("processing_class" in form.fields)
