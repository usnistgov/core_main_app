"""Query builder class
"""
from bson.objectid import ObjectId
from core_main_app.utils.query.mongo.prepare import prepare_query
import json


class QueryBuilder(object):
    """Query builder class
    """

    def __init__(self, query, sub_document_root):
        """Creates query builder

        Args:
            query:
            sub_document_root:
        """
        self.criteria = [prepare_query(json.loads(query),
                                       regex=True,
                                       sub_document_root=sub_document_root)]

    def add_list_templates_criteria(self, list_template_ids):
        """Adds a criteria on template ids

        Args:
            list_template_ids:

        Returns:

        """
        self.criteria.append({'template': {'$in': [ObjectId(template_id) for template_id in list_template_ids]}})

    def get_raw_query(self):
        """Returns the raw query

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
