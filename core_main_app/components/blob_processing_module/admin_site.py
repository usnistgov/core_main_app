"""Custom admin site for the Blob Module model"""

from core_main_app.components.abstract_processing_module.admin_site import (
    AbstractProcessingModuleAdmin,
)
from core_main_app.components.blob_processing_module.forms import (
    BlobProcessingModuleForm,
)


class BlobProcessingModuleAdmin(AbstractProcessingModuleAdmin):
    form = BlobProcessingModuleForm
