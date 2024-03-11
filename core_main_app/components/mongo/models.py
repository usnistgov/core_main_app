""" Mongoengine Data model
"""
import logging

from django.conf import settings

from core_main_app.commons.exceptions import CoreError
from core_main_app.components.data.models import Data
from core_main_app.components.data.tasks import (
    index_mongo_data,
    delete_mongo_data,
    update_mongo_data_user,
    update_mongo_data_workspace,
)
from core_main_app.components.template.models import Template
from core_main_app.components.workspace.models import Workspace
from core_main_app.settings import (
    SEARCHABLE_DATA_OCCURRENCES_LIMIT,
    XML_POST_PROCESSOR,
    XML_FORCE_LIST,
)
from core_main_app.utils import xml as xml_utils
from core_main_app.utils.json_utils import load_json_string

logger = logging.getLogger(__name__)

try:
    if settings.MONGODB_INDEXING:
        from bson import ObjectId
        from mongoengine import Document, DoesNotExist
        from mongoengine import fields as mongo_fields

        class AbstractMongoData(Document):
            """Data object stored in MongoDB"""

            data_id = mongo_fields.IntField(primary_key=True)
            title = mongo_fields.StringField()
            dict_content = mongo_fields.DictField()
            creation_date = mongo_fields.DateTimeField()
            last_modification_date = mongo_fields.DateTimeField()
            last_change_date = mongo_fields.DateTimeField()
            mongo_id = mongo_fields.ObjectIdField()

            meta = {
                "abstract": True,
            }

            def get_dict_content(self):
                """Return dict_content

                Returns:

                """
                return self.dict_content

            @staticmethod
            def post_save_data(sender, instance, **kwargs):
                """post_save_data

                Args:
                    sender:
                    instance:
                    kwargs:

                Returns:

                """
                raise NotImplementedError("post_save_data not implemented")

            @staticmethod
            def post_delete_data(sender, instance, **kwargs):
                """post_delete_data

                Args:
                    sender:
                    instance:
                    kwargs:

                Returns:

                """
                raise NotImplementedError("post_delete_data not implemented")

        class MongoData(AbstractMongoData):
            """Data object stored in MongoDB"""

            _template_id = mongo_fields.IntField(db_field="template")
            user_id = mongo_fields.IntField()
            _workspace_id = mongo_fields.IntField(db_field="workspace")
            _content = None

            meta = {
                "indexes": [
                    "title",
                    "_template_id",
                    "user_id",
                    "last_modification_date",
                ],
            }

            @property
            def template(self):
                """Return template object

                Returns:

                """
                return Template.get_by_id(self._template_id)

            @property
            def _blob(self):
                """Return blob object

                Returns:

                """
                try:
                    return Data.get_by_id(self.data_id)._blob
                except Exception:
                    logger.error("Unable to get MongoData._blob")
                    return None

            def blob(self, user):
                """Return blob object

                Args:
                    user:

                Returns:

                """
                return Data.get_by_id(self.data_id).blob(user)

            @property
            def template_id(self):
                """Return template id

                Returns:

                """
                return self._template_id

            @property
            def workspace(self):
                """Return workspace object

                Returns:

                """
                return (
                    Workspace.get_by_id(self._workspace_id)
                    if self._workspace_id
                    else None
                )

            @property
            def content(self):
                """Get xml content - read from data.

                Returns:

                """
                if not self._content:
                    self._content = Data.get_by_id(self.data_id).content
                return self._content

            @content.setter
            def content(self, value):
                """Set xml content - to be saved as a file.

                Args:
                    value:

                Returns:

                """
                self._content = value

            @property
            def xml_content(self):
                """Get content - backward compatibility"""
                return self.content

            @xml_content.setter
            def xml_content(self, value):
                """Set content - backward compatibility"""
                self.content = value

            @staticmethod
            def execute_query(query, order_by_field):
                """Execute a query.

                Args:
                    query:
                    order_by_field: Order by field.

                Returns:

                """
                return MongoData.objects.filter(query).order_by(
                    *order_by_field
                )

            @staticmethod
            def aggregate(pipeline):
                """Execute an aggregate on the Data collection.

                Args:
                    pipeline:

                Returns:

                """
                return MongoData.objects().aggregate(pipeline)

            @staticmethod
            def init_mongo_data(data):
                """Initialize mongo data from data

                Args:
                    data:

                Returns:

                """
                try:
                    # check if data already exists in mongo
                    mongo_data = MongoData.objects.get(pk=data.id)
                except DoesNotExist:
                    # create new mongo data otherwise
                    mongo_data = MongoData()
                    mongo_data.mongo_id = ObjectId()
                # Get template
                data_template = data.template
                # Initialize mongo data fields
                mongo_data.data_id = data.id
                mongo_data.title = data.title
                if data_template.format == Template.JSON:
                    # store python dict
                    mongo_data.dict_content = load_json_string(data.content)
                elif data_template.format == Template.XSD:
                    # transform xml content into a dictionary
                    mongo_data.dict_content = xml_utils.raw_xml_to_dict(
                        data.xml_content,
                        postprocessor=XML_POST_PROCESSOR,
                        force_list=XML_FORCE_LIST,
                        list_limit=SEARCHABLE_DATA_OCCURRENCES_LIMIT,
                    )

                mongo_data._template_id = (
                    data_template.id if data_template else None
                )
                mongo_data.user_id = data.user_id if data.user_id else None
                mongo_data._workspace_id = (
                    data.workspace.id if data.workspace else None
                )
                mongo_data.creation_date = data.creation_date
                mongo_data.last_modification_date = data.last_modification_date
                mongo_data.last_change_date = data.last_change_date
                return mongo_data

            @staticmethod
            def update_user_id_from_queryset(data_queryset, user_id):
                """Update user id of all data in queryset

                Args:
                    data_queryset:
                    user_id:

                Returns:

                """
                data_ids = data_queryset.values_list("id", flat=True)
                if settings.MONGODB_ASYNC_SAVE:
                    update_mongo_data_user.apply_async(
                        (
                            list(data_ids),
                            user_id,
                        )
                    )
                else:
                    for data_id in data_ids:
                        mongo_data = MongoData.objects.get(pk=data_id)
                        mongo_data.user_id = user_id
                        mongo_data.save()

            @staticmethod
            def update_workspace_id_from_queryset(data_queryset, workspace_id):
                """Update workspace id of all data in queryset

                Args:
                    data_queryset:
                    workspace_id:

                Returns:

                """
                data_ids = data_queryset.values_list("id", flat=True)
                if settings.MONGODB_ASYNC_SAVE:
                    update_mongo_data_workspace.apply_async(
                        (
                            list(data_ids),
                            workspace_id,
                        )
                    )
                else:
                    for data_id in data_ids:
                        mongo_data = MongoData.objects.get(pk=data_id)
                        mongo_data._workspace_id = workspace_id
                        mongo_data.save()

            @staticmethod
            def post_save_data(sender, instance, **kwargs):
                """Method executed after saving of Data.
                Args:
                    sender: Class.
                    instance: Data document.
                    **kwargs: Args.

                """
                if settings.MONGODB_ASYNC_SAVE:
                    index_mongo_data.apply_async((str(instance.id),))
                else:
                    mongo_data = MongoData.init_mongo_data(instance)
                    mongo_data.save()

            @staticmethod
            def post_delete_data(sender, instance, **kwargs):
                """Method executed after deleting a Data.
                Args:
                    sender: Class.
                    instance: Data document.
                    **kwargs: Args.

                """
                if settings.MONGODB_ASYNC_SAVE:
                    delete_mongo_data.apply_async((str(instance.id),))
                else:
                    try:
                        mongo_data = MongoData.objects.get(data_id=instance.id)
                        mongo_data.delete()
                    except DoesNotExist:
                        logger.warning(
                            f"Trying to delete {str(instance.id)} but document was not found."
                        )
                    except Exception as e:
                        logger.error(f"An unexpected error occurred: {str(e)}")

            @staticmethod
            def pre_delete_workspace(sender, instance, **kwargs):
                """Method executed before deleting a Workspace.
                Args:
                    sender: Class.
                    instance: Workspace document.
                    **kwargs: Args.

                """
                queryset = Data.objects.filter(workspace=instance.id).all()
                MongoData.update_workspace_id_from_queryset(queryset, None)

except ImportError:
    raise CoreError(
        "Mongoengine needs to be installed when MongoDB indexing is enabled. "
        "Install required python packages (see requirements.mongo.txt) "
        "or disable MongoDB indexing (MONGODB_INDEXING=False). "
    )
