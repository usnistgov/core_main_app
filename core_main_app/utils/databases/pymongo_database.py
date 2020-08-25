"""
    The Database pymongo tool contains the available function relative to database operation (connection)
"""
import logging
import re

from pymongo import MongoClient
from pymongo.errors import OperationFailure

from core_main_app.commons import exceptions

logger = logging.getLogger(__name__)


class Database(object):
    """Represent Database."""

    def __init__(self):
        self.client = None

    def connect(self, db_uri, db_name, doc_class=dict):
        """Connect to the database from settings.py.

        Args:
            db_uri:
            db_name:
            doc_class:

        Returns:

        """
        # create a connection
        self.client = MongoClient(db_uri, document_class=doc_class)
        db = self.client[db_name]  # connect to the database
        if db is not None:
            return db  # return db connection
        else:  # or raise an exception
            raise exceptions.CoreError("Database connection error")

    def close_connection(self):
        """
        Close the client connection.
        """
        self.client.close()

    @staticmethod
    def get_collection(db, collection_name):
        """Return cursor of collection name in parameters.

        Args:
            db:
            collection_name:

        Returns:

        """
        try:
            data_list = db[collection_name]  # get the data collection
            return data_list  # return collection
        except:  # or raise an exception
            raise exceptions.CoreError("Collection in database does not exist")

    @staticmethod
    def clean_database(db):
        """Clean the database.

        Args:
            db:

        Returns:

        """
        # clear all collections
        for collection in db.list_collection_names():
            try:
                if collection != "system.indexes":
                    db.drop_collection(collection)
            except OperationFailure as e:
                logger.warning("clean_database threw an exception: ".format(str(e)))


def get_full_text_query(text):
    """Return a full text query.

    Args:
        text: List of keywords

    Returns: The corresponding query

    """
    full_text_query = {}
    word_list = re.sub("[^\w]", " ", text, flags=re.UNICODE).split()
    word_list = ['"' + x + '"' for x in word_list]
    word_list = " ".join(word_list)
    if len(word_list) > 0:
        full_text_query = {"$text": {"$search": word_list}}

    return full_text_query
