""" Mongo engine database tools
"""
from mongoengine import connect


class Database(object):
    """ Represent Database
    """

    def __init__(self, host, name):
        """ Constructor of the database Object

        Args:
            host: host of the database (like an uri)
            name: name of the database
        """
        self.database_host = host
        self.database_name = name
        self.database = None

    def connect(self):
        """ Open an connection to the database

        Returns:
            the database connection created
        """
        self.database = connect(self.database_name, host=self.database_host)
        return self.database

    def clean_database(self):
        """ Drop the database

                Returns:

                """
        # clear the mock database for the next test
        if self.database is not None:
            self.database.drop_database(self.database_name)
        self.database = None
