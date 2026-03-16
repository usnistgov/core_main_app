"""Model for data processing modules."""

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.components.abstract_processing_module.models import (
    AbstractProcessingModule,
)


class DataProcessingModule(AbstractProcessingModule):
    """Class managing data processing modules"""

    template_filename_regexp = models.CharField(
        max_length=250, default=".*"  # noqa
    )  # ".*" ".*\.json"

    @staticmethod
    def get_by_id(data_module_id):
        """Return the data processing modules with the given id.

        Args:
            data_module_id:

        Returns:
            Data Processing Module

        """
        try:
            return DataProcessingModule.objects.get(pk=data_module_id)
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_all():
        """Return all data processing modules.

        Args:

        Returns:
            List of Data instances.

        """
        return DataProcessingModule.objects.all()
