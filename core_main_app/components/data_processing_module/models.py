"""Model for data processing modules."""

from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction

from core_main_app.commons import exceptions
from core_main_app.components.abstract_processing_module.models import (
    AbstractProcessingModule,
)
from core_main_app.components.data_processing_module.context import (
    _suppress_processing_signals,
)


class DataProcessingModule(AbstractProcessingModule):
    """Class managing data processing modules"""

    template_filename_regexp = models.CharField(
        max_length=250, default=".*"  # noqa
    )  # ".*" ".*\.json"

    def _guarded_save(self, data):
        """Save data and prevent recursion"""
        token = _suppress_processing_signals.set(True)
        try:
            data.convert_and_save()
        finally:
            _suppress_processing_signals.reset(token)

    def execute_process(self, data, *args, **kwargs):
        """Execute the processing module and defer save if content changed"""
        original_content = data.content
        processor = self.get_class()
        processor.process(data, *args, **kwargs)

        if kwargs["strategy"] != "DELETE" and data.content != original_content:
            transaction.on_commit(lambda: self._guarded_save(data))

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
