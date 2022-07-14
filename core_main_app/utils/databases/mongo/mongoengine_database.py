""" Mongoengine database tools
"""
from mongoengine import connect
from mongoengine.connection import disconnect


class Database:
    """Represent a Database."""

    def __init__(self, host, name):
        """Constructor of the database Object

        Args:
            host: host of the database (like an uri)
            name: name of the database
        """
        self.database_host = host
        self.database_name = name
        self.database = None

    def connect(self):
        """Open a connection to the database.

        Returns:
            the database connection created
        """
        self.database = connect(self.database_name, host=self.database_host)
        return self.database

    def disconnect(self):
        """Close the connection."""
        disconnect(self.database)

    def clean_database(self):
        """Clear all collections of the database.

        Returns:

        """
        # Clear the database for the next test
        if self.database[self.database_name] is not None:
            # Clear all collections
            for collection in self.database[self.database_name].list_collection_names():
                if collection != "system.indexes":
                    # WARNING: Do not drop the collection but clear it. Drop collection with mongomock is not well
                    # supported. Please see https://github.com/mongomock/mongomock/issues/238
                    self.database[self.database_name].get_collection(
                        collection
                    ).delete_many({})
