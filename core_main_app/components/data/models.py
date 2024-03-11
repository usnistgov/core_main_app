""" Data model
"""

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.indexes import GinIndex
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.db.models import Q

from core_main_app.access_control.decorators import access_control
from core_main_app.commons import exceptions
from core_main_app.commons.constants import (
    DATA_FILE_CONTENT_TYPE_FOR_TEMPLATE_FORMAT,
)
from core_main_app.commons.exceptions import ModelError
from core_main_app.components.abstract_data.models import AbstractData
from core_main_app.components.blob.models import Blob
from core_main_app.components.data.access_control import can_read_blob
from core_main_app.components.template.models import Template
from core_main_app.components.workspace.models import Workspace
from core_main_app.settings import (
    SEARCHABLE_DATA_OCCURRENCES_LIMIT,
    XML_POST_PROCESSOR,
    XML_FORCE_LIST,
)
from core_main_app.utils import xml as xml_utils
from core_main_app.utils.json_utils import load_json_string


# TODO: Create publication workflow manager
# TODO: execute_query / execute_query_full_result -> use find method (RETURN FULL OBJECT)


class Data(AbstractData):
    """Data object"""

    template = models.ForeignKey(
        Template, blank=False, on_delete=models.CASCADE
    )
    user_id = models.CharField(blank=False, max_length=200)
    workspace = models.ForeignKey(
        Workspace, blank=True, on_delete=models.SET_NULL, null=True
    )
    _blob = models.ForeignKey(
        Blob,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="_metadata",
    )

    class Meta:
        """Meta"""

        verbose_name = "Data"
        verbose_name_plural = "Data"
        indexes = [
            models.Index(
                fields=[
                    "title",
                    "last_modification_date",
                    "template",
                    "user_id",
                ]
            ),
            GinIndex(fields=["vector_column"]),
        ]

    def convert_to_dict(self):
        """Convert the xml contained in content into a dictionary.

        Returns:

        """
        # if data stored in mongo, don't store dict_content
        if settings.MONGODB_INDEXING:
            return

        if self.template.format == Template.JSON:
            # transform json string format into a dictionary.
            self.dict_content = load_json_string(self.content)

        elif self.template.format == Template.XSD:
            # transform xml content into a dictionary.
            self.dict_content = xml_utils.raw_xml_to_dict(
                self.content,
                postprocessor=XML_POST_PROCESSOR,
                force_list=XML_FORCE_LIST,
                list_limit=SEARCHABLE_DATA_OCCURRENCES_LIMIT,
            )
        else:
            raise ModelError("Unrecognized file format.")

    def convert_to_file(self):
        """Convert the xml string into a file.

        Returns:

        """
        # Check if known format
        if self.template.format not in [Template.JSON, Template.XSD]:
            raise ModelError("Unrecognized file format.")

        # Set content-type
        content_type = DATA_FILE_CONTENT_TYPE_FOR_TEMPLATE_FORMAT[
            self.template.format
        ]
        # Get content
        try:
            content = self.content.encode("utf-8")
        except UnicodeEncodeError:
            content = self.content

        self.file = SimpleUploadedFile(
            name=self.title,
            content=content,
            content_type=content_type,
        )

    @property
    def owner_name(self):
        """Get owner name

        Returns:

        """
        return User.objects.get(pk=self.user_id).username

    @access_control(can_read_blob)
    def blob(self, user):
        """

        Args:
            user:

        Returns:

        """
        return self._blob

    def get_dict_content(self):
        """Get dict_content from object or from MongoDB

        Returns:

        """
        if settings.MONGODB_INDEXING:
            from core_main_app.components.mongo.models import MongoData

            return MongoData.objects.get(pk=self.id).dict_content
        return self.dict_content

    @staticmethod
    def get_all(order_by_field):
        """Get all data.

        Args:
            order_by_field: Order by field.

        Returns:

        """
        return Data.objects.all().order_by(
            *[field.replace("+", "") for field in order_by_field]
        )

    @staticmethod
    def get_all_except(order_by_field, id_list=None):
        """Get all data except for the ones with ID within the provided list.

        Args:
            id_list:
            order_by_field:

        Returns:
        """
        if id_list is None:
            return Data.get_all(
                [field.replace("+", "") for field in order_by_field]
            )

        return Data.objects.exclude(pk__in=id_list).order_by(
            *[field.replace("+", "") for field in order_by_field]
        )

    @staticmethod
    def get_all_by_user_id(user_id, order_by_field):
        """Get all data relative to the given user id

        Args:
            user_id:
            order_by_field: Order by field.

        Returns:

        """
        return Data.objects.filter(user_id=str(user_id)).order_by(
            *[field.replace("+", "") for field in order_by_field]
        )

    @staticmethod
    def get_all_except_user_id(user_id, order_by_field):
        """Get all data non relative to the given user id

        Args:
            user_id:
            order_by_field:

        Returns:

        """
        return Data.objects.exclude(user_id__in=str(user_id)).order_by(
            *[field.replace("+", "") for field in order_by_field]
        )

    @staticmethod
    def get_all_by_id_list(list_id, order_by_field):
        """Return the object with the given list id.

        Args:
            list_id:
            order_by_field:

        Returns:
            Object collection
        """
        return Data.objects.filter(pk__in=list_id).order_by(
            *[field.replace("+", "") for field in order_by_field]
        )

    @staticmethod
    def get_by_id(data_id):
        """Return the object with the given id.

        Args:
            data_id:

        Returns:
            Data (obj): Data object with the given id

        """
        try:
            return Data.objects.get(pk=data_id)
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def execute_query(query, order_by_field):
        """Execute a query.

        Args:
            query:
            order_by_field: Order by field.

        Returns:

        """
        return (
            Data.objects.filter(query)
            .order_by(*[field.replace("+", "") for field in order_by_field])
            .all()
        )

    @staticmethod
    def get_all_by_workspace(workspace, order_by_field):
        """Get all data that belong to the workspace.

        Args:
            workspace:
            order_by_field:

        Returns:

        """

        if workspace is None:
            workspace_q = Q(workspace__isnull=True)
        else:
            workspace_q = Q(workspace=workspace)
        return Data.objects.filter(workspace_q).order_by(
            *[field.replace("+", "") for field in order_by_field]
        )

    @staticmethod
    def get_all_by_list_template(list_template, order_by_field):
        """Get all data that belong to the list of template.

        Args:
            list_template:
            order_by_field:

        Returns:

        """
        return Data.objects.filter(template__in=list_template).order_by(
            *[field.replace("+", "") for field in order_by_field]
        )

    @staticmethod
    def get_none():
        """Return None object, used by data.

        Returns:

        """
        return Data.objects.none()

    def __str__(self):
        """Return Data object as string

        Returns:

        """
        return self.title
