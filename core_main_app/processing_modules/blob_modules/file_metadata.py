""" Blob processing module to maintain file metadata about a blob.
"""

import json
from copy import deepcopy
from pathlib import Path

from django.urls import reverse

from core_main_app.commons.exceptions import CoreError
from core_main_app.components.data.models import Data
from core_main_app.settings import SERVER_URI
from core_main_app.system import api as system_api
from core_main_app.system.blob import api as blob_system_api
from core_main_app.utils import datetime
from core_main_app.utils.processing_module.models import (
    AbstractObjectProcessing,
)


class FileMetadataBlobProcessing(AbstractObjectProcessing):
    """Class containing all processing functions to maintain file metadata about a blob."""

    @staticmethod
    def _get_metadata_title(blob_filename):
        """Get metadata title

        Args:
            blob_filename:

        Returns:

        """
        return f"{Path(blob_filename).with_suffix('')} metadata"

    @staticmethod
    def _get_current_time():
        """Get current time

        Returns:

        """
        return datetime.datetime_to_utc_datetime_iso8601(
            datetime.datetime_now()
        )

    @staticmethod
    def _get_blob_detail_url(blob_id):
        """Get blob detail url

        Args:
            blob_id:

        Returns:

        """
        return (
            f"{SERVER_URI}{reverse('core_main_app_blob_detail')}?id={blob_id}"
        )

    def create_metadata_file(self, blob, blob_module_params):  # noqa
        """Create a metadata file

        Args:
            blob:
            blob_module_params:

        Returns:

        """
        current_time = self.__class__._get_current_time()

        blob_info_dict = {
            "filename": blob.filename,
            "checksum": blob.checksum,
            "url": self.__class__._get_blob_detail_url(blob.pk),
            "size": blob.size,
            "dates": {
                "creation_date": current_time,
                "modification_date": current_time,
            },
        }
        # create new data
        data = Data(
            title=self.__class__._get_metadata_title(blob.filename),
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

    def update_metadata_file(self, blob, blob_module_params):
        """Update the metadata file

        Args:
            blob:
            blob_module_params:

        Returns:

        """
        # Check if metadata files with the correct name already exists.
        metadata_data_list = [
            metadata_data
            for metadata_data in Data.objects.filter(_blob=blob)
            if metadata_data.title
            == self.__class__._get_metadata_title(blob.filename)
        ]

        metadata_data_list_size = len(metadata_data_list)

        if (
            metadata_data_list_size == 0
        ):  # If no metadata files are found, create one.
            return self.create_metadata_file(blob, blob_module_params)
        elif (
            metadata_data_list_size > 1
        ):  # Too many metadata files with the same name.
            raise CoreError(
                "Too many metadata file found. Expecting at most 1 file, found "
                f"{metadata_data_list_size}."
            )

        metadata_data = metadata_data_list[0]
        metadata_data_dict_content = deepcopy(metadata_data.get_dict_content())
        metadata_data_dict_content["dates"][
            "modification_date"
        ] = self.__class__._get_current_time()

        metadata_data.content = json.dumps(metadata_data_dict_content)
        return system_api.upsert_data(metadata_data)

    def delete_metadata_file(self, blob, blob_module_params):
        """Delete metadata file

        Args:
            blob:
            blob_module_params:

        Returns:

        """
        # Check if metadata files with the correct name already exists.
        metadata_data_list = [
            metadata_data
            for metadata_data in Data.objects.filter(_blob=blob)
            if metadata_data.title
            == self.__class__._get_metadata_title(blob.filename)
        ]

        metadata_data_list_size = len(metadata_data_list)

        if (
            metadata_data_list_size == 0
        ):  # If no metadata files are found, return.
            return
        elif (
            metadata_data_list_size > 1
        ):  # Too many metadata files with the same name.
            raise CoreError(
                "Too many metadata file found. Expecting at most 1 file, found "
                f"{metadata_data_list_size}."
            )

        metadata_data_list[0].delete()

    def _process_on_create(self, blob, blob_module_params):
        """Method to perform processing when the blob is created.

        Args:
            blob:
            blob_module_params:
        """
        return self.create_metadata_file(blob, blob_module_params)

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
        return self.update_metadata_file(blob, blob_module_params)

    def _process_on_delete(self, blob, blob_module_params):
        """Method to perform processing when the blob is deleted.

        Args:
            blob:
            blob_module_params:
        """
        return self.delete_metadata_file(blob, blob_module_params)

    def _process_on_demand(self, blob, blob_module_params):
        """Method to perform processing when triggered by the user.

        Args:
            blob:
            blob_module_params:
        """
        return self.update_metadata_file(blob, blob_module_params)
