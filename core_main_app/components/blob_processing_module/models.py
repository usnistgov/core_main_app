""" Model for blob processing modules.
"""

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.components.abstract_processing_module.models import (
    AbstractProcessingModule,
)


class BlobProcessingModule(AbstractProcessingModule):
    """Class managing blob processing modules"""

    blob_filename_regexp = models.CharField(
        max_length=250, validators=[RegexValidator], default=".*"
    )  # ".*" ".+\.[xml,json]"

    @staticmethod
    def get_by_id(blob_id):
        """Return the blob processing modules with the given id.

        Args:
            blob_id:

        Returns:
            Blob

        """
        try:
            return BlobProcessingModule.objects.get(pk=blob_id)
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_all():
        """Return all blobs processing modules.

        Args:

        Returns:
            List of Blob instances.

        """
        return BlobProcessingModule.objects.all()
