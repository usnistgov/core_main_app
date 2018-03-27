""" Fixtures files for Blobs
"""
from core_main_app.components.blob.models import Blob
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface


class BlobFixtures(FixtureInterface):
    """ Blob fixtures
    """
    blob_1 = None
    blob_2 = None
    blob_3 = None
    blob_collection = None

    def insert_data(self):
        """ Insert a set of Blobs.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_blob_collection()

    def generate_blob_collection(self):
        """ Generate a Blob collection.

        Returns:

            user 1 -> blob1, blob2
            user 2 -> blob3

        """
        # NOTE: no real file to avoid using unsupported GridFS mock
        self.blob_1 = Blob(filename='blob1',
                           user_id='1',
                           handle='handle1').save()
        self.blob_2 = Blob(filename='blob2',
                           user_id='1',
                           handle='handle2').save()
        self.blob_3 = Blob(filename='blob3',
                           user_id='2',
                           handle='handle3').save()

        self.blob_collection = [self.blob_1,
                                self.blob_2,
                                self.blob_3]
