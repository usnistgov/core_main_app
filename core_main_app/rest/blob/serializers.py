"""
    Serializers used throughout the Rest API
"""
from rest_framework.exceptions import ValidationError
from rest_framework.fields import FileField, SerializerMethodField
from rest_framework_mongoengine.fields import ReferenceField
from rest_framework_mongoengine.serializers import DocumentSerializer

import core_main_app.components.blob.api as blob_api
from core_main_app.components.blob.models import Blob
from core_main_app.components.blob.utils import get_blob_download_uri


class BlobSerializer(DocumentSerializer):
    """ Blob serializer
    """
    blob = FileField(write_only=True)
    handle = SerializerMethodField()
    upload_date = SerializerMethodField()

    class Meta:
        model = Blob
        fields = ['id',
                  'user_id',
                  'handle',
                  'blob',
                  'upload_date']
        read_only_fields = ('id', 'user_id', 'handle', 'upload_date',)

    def get_handle(self, instance):
        """ Return handle

        Args:
            instance:

        Returns:

        """
        # get request from context
        request = self.context.get('request')
        # return download handle
        return get_blob_download_uri(instance, request)

    def get_upload_date(self, instance):
        """ Return upload date

        Args:
            instance:

        Returns:

        """
        # Return instance generation time
        return str(instance.id.generation_time)

    def create(self, validated_data):
        """ Create and return a new `Blob` instance, given the validated data.

        Args:
            validated_data:

        Returns:

        """
        # Create blob
        blob_object = Blob(filename=validated_data['blob'].name,
                           user_id=str(validated_data['user'].id))
        # Set file content
        blob_object.blob = validated_data['blob'].file

        # Save the blob
        return blob_api.insert(blob_object)


class DeleteBlobsSerializer(DocumentSerializer):
    """ Delete Blob serializer.
    """
    id = ReferenceField(Blob)

    class Meta:
        model = Blob
        fields = ('id', )

    def validate_id(self, blob):
        """ Validate id field

        Args:
            blob:

        Returns:

        """
        request = self.context.get('request')
        blob_object = blob_api.get_by_id(blob.id)

        if str(request.user.id) != blob_object.user_id or not request.user.is_superuser:
            raise ValidationError("Unauthorized")

        return blob.id
