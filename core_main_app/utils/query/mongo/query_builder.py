"""Query builder class
"""
import json
import logging

from core_main_app.components.workspace import api as workspace_api
from core_main_app.utils.query.constants import (
    VISIBILITY_PUBLIC,
    VISIBILITY_ALL,
    VISIBILITY_USER,
)
from core_main_app.utils.query.mongo.prepare import prepare_query

logger = logging.getLogger(__name__)


class QueryBuilder:
    """Query builder class"""

    def __init__(self, query, sub_document_root):
        """Create query builder

        Args:
            query:
            sub_document_root:
        """
        try:
            # try to load the query in Json
            # in case the user give a query in string format
            query = json.loads(query)
        except TypeError as exception:
            # if type error, we use the query as is
            # (the query must be directly given in json format)
            # Log the exception
            logger.warning(str(exception))

        self.criteria = [
            prepare_query(query, regex=True, sub_document_root=sub_document_root)
        ]

    def add_list_criteria(self, object_name, list_ids):
        """Add a criteria on template ids

        Args:
            object_name
            list_ids:

        Returns:

        """
        criteria_ids = []
        for object_id in list_ids:
            if object_id == "None":
                criteria_ids.append(None)
            else:
                criteria_ids.append(object_id)

        self.criteria.append({object_name: {"$in": criteria_ids}})

    def add_visibility_criteria(self, visibility):
        """Add a criteria on visibility

        Args:
            visibility:

        Returns:

        """
        if visibility == VISIBILITY_PUBLIC:
            self.criteria.append(
                {
                    "workspace": {
                        "$in": [
                            workspace_id
                            for workspace_id in workspace_api.get_all_public_workspaces().values_list(
                                "id", flat=True
                            )
                        ]
                    }
                }
            )
        elif visibility == VISIBILITY_ALL:
            # NOTE: get all data, no restriction needed
            logger.info("add_visibility_criteria case not implemented.")
        elif visibility == VISIBILITY_USER:
            # TODO: get only user data
            logger.info("add_visibility_criteria case not implemented.")

    def add_title_criteria(self, title):
        """Add a criteria on title

        Args:
            title:

        Returns:

        """
        self.criteria.append({"title": title})

    def get_raw_query(self):
        """Return the raw query

        Returns:

        """
        # create a raw query
        if len(self.criteria) > 1:
            # more than one criteria, create a AND query
            raw_query = {"$and": self.criteria}
        else:
            # one criteria, raw query is the criteria
            raw_query = self.criteria[0]

        return raw_query
