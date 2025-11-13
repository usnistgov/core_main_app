""" Data Processing Module Forms test class
"""

from unittest import TestCase

from core_main_app.components.data_processing_module.forms import (
    DataProcessingModuleForm,
)


class TestDataProcessingModuleForm(TestCase):
    """TestDataProcessingModuleForm"""

    def test_DataProcessingModuleForm(self):
        """test_DataProcessingModuleForm

        Returns:

        """

        form = DataProcessingModuleForm()
        self.assertTrue("run_strategy_list" in form.fields)
        self.assertTrue("parameters" in form.fields)
        self.assertTrue("processing_class" in form.fields)
