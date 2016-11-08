"""
    Data model
"""
from core_main_app.utils.database import Database
from core_main_app.commons import exceptions
from collections import OrderedDict
from bson.objectid import ObjectId
from pymongo import TEXT

import re

# TODO: Create publication workflow manager
# TODO: execute_query / execute_query_full_result -> use find method (RETURN FULL OBJECT)
# TODO: Delete method have to be moved
# TODO: update_publish / update_unpublish have to be move in OAI
# TODO: Status class have to be move to Core/Common/Enums.py


class Data(object):
    """
        Wrapper to manage JSON Documents, like mongoengine would have manage them (but with ordered data)
    """

    def __init__(self, template_id=None, content=None, title="", user_id=None):
        """
            initialize the object
            template_id = ref template (Document)
            title = title of the document
            json = content in json format
            id_user = user linked
        """
        self.database = Database()
        self.content = OrderedDict()                    # create a new dict to keep the mongoengine order

        if isinstance(template_id, basestring):
            self.content['template_id'] = template_id   # insert the ref to schema
        else:
            raise exceptions.DataModelError("template must be a string value")

        if isinstance(title, basestring):
            self.content['title'] = title               # insert the title
        else:
            raise exceptions.DataModelError("title must be a string value")

        if isinstance(content, OrderedDict):
            self.content['content'] = content           # insert the json content
        else:
            raise exceptions.DataModelError("content must be OrderedDict value")

        if isinstance(user_id, basestring):
            self.content['user_id'] = user_id           # insert the user id
        else:
            raise exceptions.DataModelError("user_id must be a string value")

    def save(self):
        """
            save into mongo db
        """
        data_collection = self.database.connect_to_collection(collection_name='data')
        doc_id = data_collection.insert(self.content)
        return_value = Data.get_by_id(doc_id)
        self.database.close_connection()
        return return_value

    @staticmethod
    def update(post_id, json_full_object=None):
        """
            Update the object with the given id
            :param post_id:
            :param json_full_object:
        """

        try:
            return Data._update_data(post_id, json_full_object)
        except:
            raise exceptions.DataModelError("Update operation error")

    @staticmethod
    def init_indexes():
        """
            Create index for full text search
        """
        database = Database()
        data_list = database.connect_to_collection('data')
        # create the full text index
        data_list.create_index([('$**', TEXT)], default_language="en", language_override="en")
        database.close_connection()

    @staticmethod
    def get_all():
        """
            returns all objects as a list of dicts
            /!\ Doesn't return the same kind of objects as mongoengine.Document.objects()
        """
        return Data.find()

    @staticmethod
    def get_all_by_user_id(user_id):
        """
            returns all objects as a list of dicts where user_id is equal to the parameter
            /!\ Doesn't return the same kind of objects as mongoengine.Document.objects()
            :param user_id:
        """
        param = {'id_user': user_id}
        return Data.find(param)

    @staticmethod
    def get_all_except_user_id(user_id):
        """
            returns all objects as a list of dicts where user_id is not equal to the parameter
            /!\ Doesn't return the same kind of objects as mongoengine.Document.objects()
            :param user_id:
        """
        param = {'id_user': {"$ne": user_id}}
        return Data.find(param)

    @staticmethod
    def get_all_by_id_list(list_id, distinct_by=None):
        """
            Returns the object with the given list id
            :param list_id:
            :param distinct_by:
        """
        database = Database()
        data_collection = database.connect_to_collection('data', db_doc_class=OrderedDict)
        list_ids = [ObjectId(x) for x in list_id]
        return_value = data_collection.find({'_id': {'$in': list_ids}}).distinct(distinct_by)
        database.close_connection()
        return return_value

    @staticmethod
    def get_by_id(post_id):
        """
            Returns the object with the given id
            :param post_id:
        """
        database = Database()
        data_collection = database.connect_to_collection('data', db_doc_class=OrderedDict)
        return_value = data_collection.find_one({'_id': ObjectId(post_id)})
        database.close_connection()
        return return_value

    @staticmethod
    def find(params=None):
        """
            returns all objects that match params as a list of dicts
            /!\ Doesn't return the same kind of objects as mongoengine.Document.objects()
            :param params:
        """
        database = Database()
        data_collection = database.connect_to_collection('data', db_doc_class=OrderedDict)
        # find all objects of the collection
        cursor = data_collection.find(params)
        database.close_connection()
        return [result for result in cursor]

    @staticmethod
    def execute_full_text_query(text, template_ids):
        """
            Execute a full text query with possible refinements
            :param text:
            :param template_ids:
            :return:
        """
        database = Database()
        data_collection = database.connect_to_collection('data', db_doc_class=OrderedDict)

        word_list = re.sub("[^\w]", " ",  text).split()
        word_list = ['"{0}"'.format(x) for x in word_list]
        word_list = ' '.join(word_list)

        if len(word_list) > 0:
            full_text_query = {'$text': {'$search': word_list}, 'schema': {'$in': template_ids}, }
        else:
            full_text_query = {'schema': {'$in': template_ids}}

        return_value = data_collection.find(full_text_query)
        database.close_connection()
        return return_value

    @staticmethod
    def _update_data(data_id=None, json_full_object=None):
        """
            Update object with the given id
            :param data_id:
            :param json_full_object:
        """
        database = Database()
        data_collection = database.connect_to_collection(collection_name='data')

        if data_id is None:
            raise exceptions.DataModelError("data_id must not be None")

        if json_full_object is None:
            raise exceptions.DataModelError("content must not be None")

        data_collection.update_one({'_id': ObjectId(data_id)}, {"$set": json_full_object}, upsert=False)
        return_value = Data.get_by_id(data_id)
        database.close_connection()
        return return_value
