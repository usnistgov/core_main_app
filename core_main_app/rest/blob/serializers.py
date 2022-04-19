"""
    Serializers used throughout the Rest API
"""
from os.path import join

from django.http import Http404
from rest_framework.fields import CharField
from rest_framework.fields import FileField, SerializerMethodField
from rest_framework_mongoengine.serializers import DocumentSerializer

import core_main_app.components.blob.api as blob_api
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.blob.models import Blob
from core_main_app.components.blob.utils import get_blob_download_uri

from django.urls import reverse
from core_main_app import settings
from urllib.parse import urljoin


class BlobSerializer(DocumentSerializer):
    """Blob serializer"""

    blob = FileField(write_only=True)
    handle = SerializerMethodField()
    upload_date = SerializerMethodField()
    if "core_linked_records_app" in settings.INSTALLED_APPS:
        pid = SerializerMethodField()

    class Meta(object):
        model = Blob
        fields = ["id", "user_id", "filename", "handle", "blob", "upload_date"]
        read_only_fields = ("id", "user_id", "filename", "handle", "upload_date")
        if "core_linked_records_app" in settings.INSTALLED_APPS:
            fields.append("pid")
            read_only_fields = read_only_fields + ("pid",)

    def get_pid(self, instance):
        """Return pid

        Args:
            instance:

        Returns:

        """
        # return pid  if assigned
        if "core_linked_records_app" not in settings.INSTALLED_APPS:
            return None
        else:
            from core_linked_records_app.components.blob import (
                api as linked_blob_api,
            )
            from core_linked_records_app.settings import ID_PROVIDER_SYSTEM_NAME

            try:
                sub_url = reverse(
                    "core_linked_records_provider_record",
                    kwargs={"provider": ID_PROVIDER_SYSTEM_NAME, "record": ""},
                )
                blob_pid = linked_blob_api.get_pid_for_blob(str(instance.id))

                return urljoin(settings.SERVER_URI, join(sub_url, blob_pid.record_name))
            except:
                return None

    def get_handle(self, instance):
        """Return handle

        Args:
            instance:

        Returns:

        """
        # get request from context
        request = self.context.get("request")
        # return download handle
        return get_blob_download_uri(instance, request)

    def get_upload_date(self, instance):
        """Return upload date

        Args:
            instance:

        Returns:

        """
        # Return instance generation time
        return str(instance.id.generation_time)

    def create(self, validated_data):
        """Create and return a new `Blob` instance, given the validated data.

        Args:
            validated_data:

        Returns:

        """
        # Create blob
        blob_object = Blob(
            filename=validated_data["blob"].name,
            user_id=str(self.context["request"].user.id),
        )
        # Set file content
        blob_object.blob = validated_data["blob"].file

        # Save the blob
        return blob_api.insert(blob_object, self.context["request"].user)


class DeleteBlobsSerializer(DocumentSerializer):
    """Delete Blob serializer."""

    id = CharField()

    class Meta(object):
        model = Blob
        fields = ("id",)

    def validate_id(self, id):
        """Validate id field

        Args:
            id:

        Returns:

        """
        request = self.context.get("request")
        try:
            blob_api.get_by_id(id, request.user)
        except DoesNotExist:
            raise Http404
        return id
