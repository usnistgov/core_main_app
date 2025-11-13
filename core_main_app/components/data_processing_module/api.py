""" Data Module API
"""

import logging

from core_main_app.access_control.api import user_is_registered
from core_main_app.access_control.decorators import access_control
from core_main_app.components.data_processing_module.models import (
    DataProcessingModule,
)
from core_main_app.components.data import api as data_api

logger = logging.getLogger(__name__)


@access_control(user_is_registered)
def get_all(user):
    """Return all data modules.

    Args:
        user:

    Returns:
        List of Data Modules.
    """
    return DataProcessingModule.get_all()


@access_control(user_is_registered)
def get_by_id(data_module_id, user):
    """Retrieve data module.

    Args:
        data_module_id:
        user:

    Returns:
        Data Module.
    """
    return DataProcessingModule.get_by_id(data_module_id)


@access_control(user_is_registered)
def get_all_by_data_id(data_id, user, run_strategy=None):
    """Retrieve data modules given a data_id.

    Args:
        data_id:
        user:
        run_strategy:

    Returns:
        List of Data Modules.
    """
    # Retrieve the data (will check ownership) and data modules.
    data_api.get_by_id(data_id, user)
    data_module_list = get_all(user)

    # Additional filtering if `run_strategy` is defined.
    data_module_list = (
        list(data_module_list.filter(run_strategy_list__contains=run_strategy))
        if run_strategy
        else data_module_list
    )

    return data_module_list
