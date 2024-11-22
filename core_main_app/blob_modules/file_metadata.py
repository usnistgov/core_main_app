""" Blob processing module to maintain file metadata about a blob.
"""

import json

from core_main_app.components.data.models import Data
from core_main_app.system import api as system_api
from core_main_app.system.blob import api as blob_system_api
from core_main_app.utils.processing_module.models import (
    AbstractObjectProcessing,
)


class FileMetadataBlobProcessing(AbstractObjectProcessing):
    """Class containing all processing functions to maintain file metadata about a blob."""

    def _process_on_create(self, blob, blob_module_params):
        """Method to perform processing when the blob is created.

        Args:
            blob:
            blob_module_params:
        """
        raise NotImplementedError(
            "Method '_process_on_create' is not yet implemented"
        )

    def _process_on_read(self, blob, blob_module_params):
        """Method to perform processing each time the blob is read.

        Args:
            blob:
            blob_module_params:
        """
        raise NotImplementedError(
            "Method '_process_on_read' is not yet implemented"
        )

    def _process_on_update(self, blob, blob_module_params):
        """Method to perform processing each time the blob is updated.

        Args:
            blob:
            blob_module_params:
        """
        raise NotImplementedError(
            "Method '_process_on_update' is not yet implemented"
        )

    def _process_on_delete(self, blob, blob_module_params):
        """Method to perform processing when the blob is deleted.

        Args:
            blob:
            blob_module_params:
        """
        raise NotImplementedError(
            "Method '_process_on_delete' is not yet implemented"
        )

    def _process_on_demand(self, blob, blob_module_params):
        """Method to perform processing when triggered by the user.

        Args:
            blob:
            blob_module_params:
        """
        blob_info_dict = {"filename": blob.filename, "size": blob.size}
        # create new data
        data = Data(
            title=blob.filename,
            template=system_api.get_template_by_id(
                blob_module_params["template_pk"],
            ),
            user_id=str(blob.user_id),
            content=json.dumps(blob_info_dict),
        )
        # save data
        system_api.upsert_data(data)
        # link data to blob
        blob_system_api.add_metadata(blob, data)
        # return data
        return data
