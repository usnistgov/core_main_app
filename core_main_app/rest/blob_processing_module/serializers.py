"""
    Serializers used throughout the Rest API
"""

import logging

from core_main_app.components.blob_processing_module.models import (
    BlobProcessingModule,
)
from rest_framework.serializers import ModelSerializer

logger = logging.getLogger(__name__)


class BlobProcessingModuleSerializer(ModelSerializer):
    """Blob serializer"""

    class Meta:
        """Meta"""

        model = BlobProcessingModule
        fields = "__all__"
