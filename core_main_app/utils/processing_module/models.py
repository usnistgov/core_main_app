""" Abstractions for processing any type of object from the database.
"""

from abc import abstractmethod

from core_main_app.commons.exceptions import CoreError
from core_main_app.components.abstract_processing_module.models import (
    AbstractProcessingModule,
)


class AbstractObjectProcessing:
    """Abstract processing module class containing all the methods to be implemented
    by a processing module.
    """

    @abstractmethod
    def _process_on_create(self, db_object, module_params):
        """Method to perform processing when the blob is created.

        Args:
            db_object:
            module_params:
        """
        raise NotImplementedError(
            "Method '_process_on_create' is not implemented."
        )

    @abstractmethod
    def _process_on_read(self, db_object, module_params):
        """Method to perform processing each time the blob is read.

        Args:
            db_object:
            module_params:
        """
        raise NotImplementedError(
            "Method '_process_on_read' is not implemented."
        )

    @abstractmethod
    def _process_on_update(self, db_object, module_params):
        """Method to perform processing each time the blob is updated.

        Args:
            db_object:
            module_params:
        """
        raise NotImplementedError(
            "Method '_process_on_update' is not implemented."
        )

    @abstractmethod
    def _process_on_delete(self, db_object, module_params):
        """Method to perform processing when the blob is deleted.

        Args:
            db_object:
            module_params:
        """
        raise NotImplementedError(
            "Method '_process_on_delete' is not implemented."
        )

    @abstractmethod
    def _process_on_demand(self, db_object, module_params):
        """Method to perform processing when triggered by the user.

        Args:
            db_object:
            module_params:
        """
        raise NotImplementedError(
            "Method '_process_on_demand' is not implemented."
        )

    def process(self, db_object, module_params: dict, strategy: str):
        """Default processing function to be called. Will forward parameter to the
        appropriate strategy function.

        Args:
            db_object:
            module_params:
            strategy:
        """
        if strategy == AbstractProcessingModule.RUN_ON_DEMAND:
            return self._process_on_demand(db_object, module_params)
        elif strategy == AbstractProcessingModule.RUN_ON_CREATE:
            return self._process_on_create(db_object, module_params)
        elif strategy == AbstractProcessingModule.RUN_ON_READ:
            return self._process_on_read(db_object, module_params)
        elif strategy == AbstractProcessingModule.RUN_ON_UPDATE:
            return self._process_on_update(db_object, module_params)
        elif strategy == AbstractProcessingModule.RUN_ON_DELETE:
            return self._process_on_delete(db_object, module_params)
        else:
            raise CoreError("Processing module strategy not found")
