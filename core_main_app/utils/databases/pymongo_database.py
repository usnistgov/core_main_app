"""
    The Database pymongo tool contains the available function relative to database operation (connection)
"""
from pymongo import MongoClient
from core_main_app.commons import exceptions
from core_main_app.settings import MONGODB_URI, DB_NAME
from pymongo import TEXT
import re


class Database(object):
    """ Represent Database
    """
    def __init__(self):
        self.client = None

    def connect(self, doc_class=dict):
        """ Connect to the database from settings.py

        Args:
            doc_class:

        Returns:

        """
        # create a connection
        self.client = MongoClient(MONGODB_URI, document_class=doc_class)
        db = self.client[DB_NAME]    # connect to the database
        if db is not None:
            return db           # return db connection
        else:                   # or raise an exception
            raise exceptions.CoreError("Database connection error")

    def connect_to_collection(self, collection_name, db_doc_class=dict):
        """
            return cursor of collection name in parameters
            :param collection_name:
            :param db_doc_class:
            :return collection
        """
        db = self.connect(doc_class=db_doc_class)    # connect to the db
        try:
            data_list = db[collection_name]     # get the data collection
            return data_list                    # return collection
        except:                                 # or raise an exception
            raise exceptions.CoreError("Collection in database does not exist")

    def close_connection(self):
        """
            Close the client connection
        """
        self.client.close()


def init_text_index(table_name):
    """ Create index for full text search
    """
    database = Database()
    data_list = database.connect_to_collection(table_name)
    # create the full text index
    data_list.create_index([('$**', TEXT)], default_language="en", language_override="en")
    database.close_connection()


def get_full_text_query(text):
    """

    Args:
        text: List of keywords

    Returns: The corresponding query

    """
    full_text_query = {}
    word_list = re.sub("[^\w]", " ", text).split()
    word_list = ['"{0}"'.format(x) for x in word_list]
    word_list = ' '.join(word_list)
    if len(word_list) > 0:
        full_text_query = {'$text': {'$search': word_list}}

    return full_text_query
