""" MongoData API
"""
from core_main_app.access_control.decorators import access_control
from core_main_app.components.data import access_control as data_api_access_control
from core_main_app.settings import DATA_SORTING_FIELDS


@access_control(data_api_access_control.can_read_data_mongo_query)
def execute_mongo_query(
    json_query, user, workspace_filter, user_filter, order_by_field=DATA_SORTING_FIELDS
):
    """

    Args:
        json_query:
        user:
        workspace_filter:
        user_filter:
        order_by_field:

    Returns:

    """
    from core_main_app.components.mongo.models import MongoData

    return MongoData.execute_query(json_query, order_by_field)


@access_control(data_api_access_control.can_read_aggregate_query)
def aggregate(pipeline, user):
    """Execute an aggregate on the Data collection.

    Args:
        pipeline:
        user:

    Returns:

    """
    from core_main_app.components.mongo.models import MongoData

    return MongoData.aggregate(pipeline)
