""" Data model
"""
from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from mongoengine import errors as mongoengine_errors
from core_main_app.utils import xml as xml_utils
from django_mongoengine import fields, Document
from core_main_app.utils.databases.pymongo_database import get_full_text_query
from core_main_app.settings import DATA_AUTO_PUBLISH

# TODO: Create publication workflow manager
# TODO: execute_query / execute_query_full_result -> use find method (RETURN FULL OBJECT)
# TODO: Delete method have to be moved
# TODO: update_publish / update_unpublish have to be move in OAI
# TODO: Status class have to be move to Core/Common/Enums.py

class Data(Document):
    """ Represents Data object
    """

    template = fields.ReferenceField(Template)
    user_id = fields.StringField()
    dict_content = fields.DictField(blank=True)
    title = fields.StringField()
    xml_file = fields.StringField()
    is_published = fields.BooleanField(blank=True, default=DATA_AUTO_PUBLISH)
    publication_date = fields.DateTimeField(blank=True, default=None)
    last_modification_date = fields.DateTimeField(blank=True, default=None)

    def convert_and_save(self):
        """ Save Data object and convert the xml to dict if needed

        Returns:

        """
        self.convert_to_dict()
        return self.save()

    def convert_to_dict(self):
        """ Convert the xml contained in xml_file to Dict

        Returns:

        """
        self.dict_content = xml_utils.raw_xml_to_dict(self.xml_file, xml_utils.post_processor)

    @staticmethod
    def get_all():
        """

        Returns:

        """
        return Data.objects.all()

    @staticmethod
    def get_all_by_user_id(user_id):
        """ Get all data relative to the given user id

        Args:
            user_id:

        Returns:

        """
        return Data.objects(user_id=str(user_id)).all()

    @staticmethod
    def get_all_except_user_id(user_id):
        """ Get all data non relative to the given user id

        Args:
            user_id:

        Returns:

        """
        return Data.objects(user_id__nin=str(user_id)).all()

    @staticmethod
    def get_all_by_id_list(list_id, distinct_by=None):
        """ Returns the object with the given list id

        Args:
            list_id:
            distinct_by:

        Returns:
            Object collection
        """
        return Data.objects(pk__in=list_id).distinct(distinct_by)

    @staticmethod
    def get_by_id(data_id):
        """ Returns the object with the given id

        Args:
            data_id:

        Returns:
            Data (obj): Data object with the given id

        """
        try:
            return Data.objects.get(pk=str(data_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)

    @staticmethod
    def execute_full_text_query(text, template_ids):
        """ Execute a full text query with possible refinements

        Args:
            text:
            template_ids:

        Returns:

        """
        query = get_full_text_query(text)
        query.update({'template__id': {'$in': template_ids}})
        return Data.objects.find(query)
