"""
    The Database tool contains the available function relative to database operation (connection)
"""
from pymongo import MongoClient
from core_main_app.commons.exceptions import MDCSError
from core_main_app.settings import MONGODB_URI, DB_NAME


class Database(object):

    def __init__(self):
        self.client = None

    def connect(self, doc_class=dict):
        """
            Connect to the database from settings.py
            :param doc_class:
            :return database connection
        """
        # create a connection
        self.client = MongoClient(MONGODB_URI, document_class=doc_class)
        db = self.client[DB_NAME]    # connect to the database
        if db is not None:
            return db           # return db connection
        else:                   # or raise an exception
            raise MDCSError("Database connection error")

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
            raise MDCSError("Collection in database does not exist")

    def close_connection(self):
        """
            Close the client connection
        """
        self.client.close()
