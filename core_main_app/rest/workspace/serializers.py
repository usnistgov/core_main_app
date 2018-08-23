"""Serializers used throughout the workspace Rest API
"""
from rest_framework_mongoengine.serializers import DocumentSerializer
from core_main_app.components.workspace.models import Workspace
from core_main_app.components.workspace import api as workspace_api


class WorkspaceSerializer(DocumentSerializer):
    """ Workspace serializer
    """
    class Meta:
        """ Meta
        """
        model = Workspace
        fields = ["id",
                  "title",
                  "owner"]
        read_only_fields = ('id', 'owner')

    def create(self, validated_data):
        """
        Create and return a new `workspace` instance, given the validated data.
        """
        return workspace_api.create_and_save(validated_data['title'], validated_data['user'].id)
