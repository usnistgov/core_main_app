""" Custom admin forms for the Blob Processing Module model
"""

from core_main_app.components.abstract_processing_module.forms import (
    AbstractProcessingModuleForm,
)
from core_main_app.components.blob_processing_module.models import (
    BlobProcessingModule,
)


class BlobProcessingModuleForm(AbstractProcessingModuleForm):
    """Model form for `BlobProcessingModuleForm` objects."""

    class Meta:
        model = BlobProcessingModule
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["blob_filename_regexp"].widget.attrs.update(
            {"placeholder": ".*"}
        )
        self.fields["parameters"].widget.attrs.update(
            {"placeholder": '{"template_pk": 42}'}
        )
        self.fields["processing_class"].widget.attrs.update(
            {
                "placeholder": "core_main_app.processing_modules.blob_modules.file_metadata.FileMetadataBlobProcessing"
            }
        )
