""" Data model
"""
from io import BytesIO

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES
from core_main_app.components.template.models import Template
from mongoengine import errors as mongoengine_errors
from core_main_app.utils import xml as xml_utils
from django_mongoengine import fields, Document

from core_main_app.utils.databases.pymongo_database import get_full_text_query
from core_main_app.settings import DATA_AUTO_PUBLISH, GRIDFS_DATA_COLLECTION, SEARCHABLE_DATA_OCCURRENCES_LIMIT


# TODO: Create publication workflow manager
# TODO: execute_query / execute_query_full_result -> use find method (RETURN FULL OBJECT)
# TODO: Delete method have to be moved
# TODO: update_publish / update_unpublish have to be move in OAI
# TODO: Status class have to be move to Core/Common/Enums.py


class Data(Document):
    """ Data object
    """
    template = fields.ReferenceField(Template)
    user_id = fields.StringField()
    dict_content = fields.DictField(blank=True)
    title = fields.StringField(blank=False, regex=NOT_EMPTY_OR_WHITESPACES)
    xml_file = fields.FileField(blank=False, collection_name=GRIDFS_DATA_COLLECTION)
    is_published = fields.BooleanField(blank=True, default=DATA_AUTO_PUBLISH)
    publication_date = fields.DateTimeField(blank=True, default=None)
    last_modification_date = fields.DateTimeField(blank=True, default=None)

    _xml_content = None

    @property
    def xml_content(self):
        """Get xml content - read from a saved file.

        Returns:

        """
        # private field xml_content not set yet, and reference to xml_file to read is set
        if self._xml_content is None and self.xml_file is not None:
            # read xml file into xml_content field
            self._xml_content = self.xml_file.read()
        # return xml content
        return self._xml_content

    @xml_content.setter
    def xml_content(self, value):
        """Set xml content - to be saved as a file.

        Args:
            value:

        Returns:

        """
        self._xml_content = value

    def convert_and_save(self):
        """ Save Data object and convert the xml to dict if needed.

        Returns:

        """
        self.convert_to_dict()
        self.convert_to_file()

        return self.save()

    def convert_to_dict(self):
        """ Convert the xml contained in xml_content into a dictionary.

        Returns:

        """
        # transform xml content into a dictionary
        dict_content = xml_utils.raw_xml_to_dict(self.xml_content, xml_utils.post_processor)
        # if limit on element occurrences is set
        if SEARCHABLE_DATA_OCCURRENCES_LIMIT is not None:
            # Remove lists which size exceed the limit size
            xml_utils.remove_lists_from_xml_dict(dict_content, SEARCHABLE_DATA_OCCURRENCES_LIMIT)
        # store dictionary
        self.dict_content = dict_content

    def convert_to_file(self):
        """ Convert the xml string into a file.

        Returns:

        """
        try:
            xml_file = BytesIO(self.xml_content.encode('utf-8'))
        except Exception:
            xml_file = BytesIO(self.xml_content)

        if self.xml_file.grid_id is None:
            # new file
            self.xml_file.put(xml_file, content_type="application/xml")
        else:
            # editing (self.xml_file gets a new id)
            self.xml_file.replace(xml_file, content_type="application/xml")

    @staticmethod
    def get_all():
        """ Get all data.

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
        """ Return the object with the given list id.

        Args:
            list_id:
            distinct_by:

        Returns:
            Object collection
        """
        return Data.objects(pk__in=list_id).distinct(distinct_by)

    @staticmethod
    def get_by_id(data_id):
        """ Return the object with the given id.

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
        """ Execute a full text query with possible refinements.

        Args:
            text:
            template_ids:

        Returns:

        """
        query = get_full_text_query(text)
        query.update({'template__id': {'$in': template_ids}})
        # TODO: does find() exist? use pymongo if not
        return Data.objects.find(query)

    @staticmethod
    def execute_query(query):
        """Execute a query.

        Args:
            query:

        Returns:

        """
        return Data.objects(__raw__=query)
