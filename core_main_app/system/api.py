""" System api
"""
from core_main_app.components.data.models import Data


def get_data_by_id(data_id):
    """ Return data object with the given id.

        Parameters:
            data_id:

        Returns: data object
    """
    return Data.get_by_id(data_id)
