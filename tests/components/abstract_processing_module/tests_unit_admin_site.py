""" Admin Site test class
"""

from unittest import TestCase

from core_main_app.components.abstract_processing_module.admin_site import (
    RunStrategyListWidget,
    AbstractProcessingModuleAdmin,
    AbstractProcessingModuleForm,
)
from core_main_app.components.blob_processing_module.models import (
    BlobProcessingModule,
)


class TestRunStrategyListWidget(TestCase):
    """TestRunStrategyListWidget"""

    def test_value_from_datadict(self):
        """test_value_from_datadict

        Returns:

        """
        widget = RunStrategyListWidget()
        self.assertEqual(
            widget.value_from_datadict(
                data=["DEMAND", "CREATE"], files=None, name=None
            ),
            '["DEMAND", "CREATE"]',
        )

    def test_render(self):
        """test_render

        Returns:

        """
        widget = RunStrategyListWidget()
        self.assertEqual(
            widget.render(
                name=None,
                value='["DEMAND", "CREATE"]',
            ),
            '<ul style="margin: 0">'
            '<li style="display: flex">'
            '<input type="checkbox" name="DEMAND" id="DEMAND" value="on" checked>'
            '<label for="DEMAND" style="margin: 0 0.25rem">Run on demand</label>'
            "</li>"
            '<li style="display: flex">'
            '<input type="checkbox" name="CREATE" id="CREATE" value="on" checked>'
            '<label for="CREATE" style="margin: 0 0.25rem">Run on create</label>'
            "</li>"
            '<li style="display: flex">'
            '<input type="checkbox" name="UPDATE" id="UPDATE" value="on">'
            '<label for="UPDATE" style="margin: 0 0.25rem">Run on update</label>'
            "</li>"
            '<li style="display: flex">'
            '<input type="checkbox" name="DELETE" id="DELETE" value="on">'
            '<label for="DELETE" style="margin: 0 0.25rem">Run on delete</label>'
            "</li>"
            "</ul>",
        )


class TestAbstractProcessingModuleForm(TestCase):
    """TestAbstractProcessingModuleForm"""

    def test_AbstractProcessingModuleForm(self):
        """test_AbstractProcessingModuleForm

        Returns:

        """

        class BlobProcessingModuleForm(AbstractProcessingModuleForm):
            class Meta:
                model = BlobProcessingModule
                fields = "__all__"

        form = BlobProcessingModuleForm()
        self.assertTrue("run_strategy_list" in form.fields)


class TestAbstractProcessingModuleAdmin(TestCase):
    """TestAbstractProcessingModuleAdmin"""

    def test_AbstractProcessingModuleAdmin(self):
        """test_AbstractProcessingModuleAdmin

        Returns:

        """
        model_admin = AbstractProcessingModuleAdmin(
            model=BlobProcessingModule, admin_site=None
        )
        self.assertEqual(model_admin.form, AbstractProcessingModuleForm)
