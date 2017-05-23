"""
    Serializers used throughout the Rest API
"""
from rest_framework.serializers import CharField, ListField
from core_main_app.commons.serializers import BasicSerializer


class DeleteBlobsSerializer(BasicSerializer):
    """ Delete Blob ids serializer
    """
    blob_ids = ListField(child=CharField())
