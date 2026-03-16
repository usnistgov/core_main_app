"""Custom admin forms for the Data Processing Module model"""

from core_main_app.components.abstract_processing_module.forms import (
    AbstractProcessingModuleForm,
)
from core_main_app.components.data_processing_module.models import (
    DataProcessingModule,
)


class DataProcessingModuleForm(AbstractProcessingModuleForm):
    """Model form for `DataProcessingModuleForm` objects."""

    class Meta:
        model = DataProcessingModule
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["template_filename_regexp"].widget.attrs.update(
            {"placeholder": ".*"}
        )
        self.fields["parameters"].widget.attrs.update(
            {"placeholder": '{"template_pk": 42}'}
        )
        self.fields["processing_class"].widget.attrs.update(
            {
                "placeholder": "core_main_app.processing_modules.data_modules.process_data"
            }
        )
