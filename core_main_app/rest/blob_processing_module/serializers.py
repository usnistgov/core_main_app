"""
    Serializers used throughout the Rest API
"""

import logging

from rest_framework.serializers import ModelSerializer

from core_main_app.components.blob_processing_module.models import (
    BlobProcessingModule,
)

logger = logging.getLogger(__name__)


class BlobProcessingModuleWriteSerializer(ModelSerializer):
    """Blob serializer"""

    class Meta:
        """Meta"""

        model = BlobProcessingModule
        fields = "__all__"


class BlobProcessingModuleReadSerializer(ModelSerializer):
    """Blob serializer"""

    class Meta:
        """Meta"""

        model = BlobProcessingModule
        fields = ["name", "run_strategy_list", "blob_filename_regexp"]
