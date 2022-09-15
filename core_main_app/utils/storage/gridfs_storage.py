""" GridFSStorage class (previously blob_utils)
"""

from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

from core_main_app.settings import (
    MONGO_DB,
    GRIDFS_STORAGE,
)

if GRIDFS_STORAGE:
    from gridfs import NoFile, GridFS

    @deconstructible
    class GridFSStorage(Storage):
        """GridFS Storage.

        Previously implemented using https://github.com/usnistgov/blob_utils/blob/master/blob_utils/gridfs_blob_host.py
        Now based on https://github.com/django-nonrel/mongodb-engine/blob/master/django_mongodb_engine/storage.py
        """

        def __init__(self, collection="fs"):
            """Initialize GridFSStorage

            Args:
                collection:
            """
            self.collection = collection

        def _open(self, name, mode="rb"):
            """Open file in read mode if exists, create a new one otherwise.

            Args:
                name:
                mode:

            Returns:

            """
            grid_fs = self._get_gridfs()
            try:
                return grid_fs.get_last_version(name)
            except NoFile:
                if "w" in mode:
                    return grid_fs.new_file(filename=name)
                else:
                    raise

        def _save(self, name, content):
            """Save the file

            Args:
                name:
                content:

            Returns:

            """
            grid_fs = self._get_gridfs()
            grid_fs.put(content, filename=name)
            return name

        def delete(self, name):
            """Delete the file

            Args:
                name:

            Returns:

            """
            grid_fs = self._get_gridfs()
            try:
                grid_fs.delete(grid_fs.get_last_version(filename=name)._id)
            except NoFile:
                pass

        def exists(self, name):
            """Check if file exists

            Args:
                name:

            Returns:

            """
            grid_fs = self._get_gridfs()
            return grid_fs.exists(filename=name)

        def size(self, name):
            """Return size of the file

            Args:
                name:

            Returns:

            """
            grid_fs = self._get_gridfs()
            return grid_fs.get_last_version(filename=name).length

        def url(self, name):
            """Url to access file (return filename to make django dashboard work).

            Args:
                name:

            Returns:
                filename to be displayed in Django dashboard

            """
            return name

        def get_created_time(self, name):
            """Get creation time

            Args:
                name:

            Returns:

            """
            grid_fs = self._get_gridfs()
            return grid_fs.get_last_version(filename=name).upload_date

        def _get_gridfs(self):
            """Get gridFS connection

            Returns:

            """
            if not hasattr(self, "_db"):
                from core_main_app.utils.databases.mongo import MONGO_CLIENT

                self._db = MONGO_CLIENT[MONGO_DB]

            return GridFS(self._db, collection=self.collection)

        def path(self, name):
            pass

        def listdir(self, path):
            pass

        def get_accessed_time(self, name):
            pass

        def get_modified_time(self, name):
            pass
