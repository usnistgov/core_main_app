""" Fixtures files for Blobs
"""
from django.core.files.uploadedfile import SimpleUploadedFile

from core_main_app.components.blob.models import Blob
from core_main_app.components.workspace.models import Workspace
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)


class BlobFixtures(FixtureInterface):
    """Blob fixtures"""

    blob_1 = None
    blob_2 = None
    blob_3 = None
    blob_collection = None

    def insert_data(self):
        """Insert a set of Blobs.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_blob_collection()

    def generate_blob_collection(self):
        """Generate a Blob collection.

        Returns:

            user 1 -> blob1, blob2
            user 2 -> blob3

        """

        self.blob_1 = Blob(
            filename="blob1",
            user_id="1",
            blob=SimpleUploadedFile("blob.txt", b"blob"),
        )
        self.blob_1.save()
        self.blob_2 = Blob(
            filename="blob2",
            user_id="1",
            blob=SimpleUploadedFile("blob.txt", b"blob"),
        )
        self.blob_2.save()
        self.blob_3 = Blob(
            filename="blob3",
            user_id="2",
            blob=SimpleUploadedFile("blob.txt", b"blob"),
        )
        self.blob_3.save()

        self.blob_collection = [self.blob_1, self.blob_2, self.blob_3]


class AccessControlBlobFixture(FixtureInterface):
    """Access Control Blob fixture"""

    USER_1_NO_WORKSPACE = 0
    USER_2_NO_WORKSPACE = 1
    USER_1_WORKSPACE_1 = 2
    USER_2_WORKSPACE_2 = 3

    workspace_1 = None
    workspace_2 = None
    workspace_without_data = None
    blob_collection = None

    def insert_data(self):
        """Insert a set of Blob.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_workspace()
        self.generate_blob_collection()

    def generate_blob_collection(self):
        """Generate a Blob collection.

        Returns:

        """
        blob_1 = Blob(filename="blob1", user_id="1")
        blob_1.save()
        blob_2 = Blob(filename="blob2", user_id="2")
        blob_2.save()
        blob_3 = Blob(
            filename="blob3",
            user_id="1",
            workspace=self.workspace_1,
        )
        blob_3.save()
        blob_4 = Blob(
            filename="blob4",
            user_id="2",
            workspace=self.workspace_2,
        )
        blob_4.save()
        self.blob_collection = [blob_1, blob_2, blob_3, blob_4]

    def generate_workspace(self):
        """Generate workspaces.

        Returns:

        """
        self.workspace_1 = Workspace(
            title="Workspace 1", owner="1", read_perm_id="1", write_perm_id="1"
        )
        self.workspace_1.save()
        self.workspace_2 = Workspace(
            title="Workspace 2", owner="2", read_perm_id="2", write_perm_id="2"
        )
        self.workspace_2.save()
        self.workspace_without_data = Workspace(
            title="Workspace 3", owner="3", read_perm_id="3", write_perm_id="3"
        )
        self.workspace_without_data.save()
