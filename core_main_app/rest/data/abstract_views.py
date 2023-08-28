""" REST abstract views for the data API
"""
import json
from abc import ABCMeta, abstractmethod

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.constants import DATA_JSON_FIELD
from core_main_app.commons.exceptions import RestApiError
from core_main_app.components.data import api as data_api
from core_main_app.settings import DATA_SORTING_FIELDS
from core_main_app.utils.query.constants import VISIBILITY_OPTION
from core_main_app.utils.query.mongo.query_builder import QueryBuilder


class AbstractExecuteLocalQueryView(APIView, metaclass=ABCMeta):
    """Abstract Execute Local Query View"""

    sub_document_root = DATA_JSON_FIELD

    def post(self, request):
        """Execute query on local instance and return results

        Parameters:

            {"query": {"$or": [{"image.owner": "Peter"}, {"image.owner.#text":"Peter"}]}}

        Args:
            request:

        Returns:

            - code: 200
              content: List of data
            - code: 400
              content: Bad request
            - code: 500
              content: Internal server error
        """
        return self.execute_query()

    def execute_query(self):
        """Compute and return query results"""
        try:
            # get query and templates
            query = self.request.data.get("query", None)
            templates = self.request.data.get("templates", [])
            if type(templates) is str:
                templates = json.loads(templates)
            workspaces = self.request.data.get("workspaces", [])
            if type(workspaces) is str:
                workspaces = json.loads(workspaces)
            options = self.request.data.get("options", {})
            if type(options) is str:
                options = json.loads(options)
            title = self.request.data.get("title", None)
            order_by_field = self.request.data.get("order_by_field", "")
            order_by_field = (
                order_by_field.split(",")
                if order_by_field
                else DATA_SORTING_FIELDS
            )
            if query is not None:
                # prepare query
                raw_query = self.build_query(
                    query=query,
                    templates=templates,
                    options=options,
                    workspaces=workspaces,
                    title=title,
                )
                # execute query
                data_list = self.execute_raw_query(raw_query, order_by_field)
                # build and return response
                return self.build_response(data_list)
            else:
                content = {"message": "Expected parameters not provided."}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except AccessControlError as acl_error:
            content = {"message": str(acl_error)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def build_query(
        self, query, workspaces=None, templates=None, options=None, title=None
    ):
        """Build the raw query

        Args:

            query: Query
            workspaces: List of workspace
            templates: List of template
            options: Query option
            title: title filter

        Returns:

            The raw query
        """
        # build query builder
        query_builder = QueryBuilder(query, self.sub_document_root)
        # update the criteria with workspaces information
        if workspaces is not None and len(workspaces) > 0:
            list_workspace_ids = [
                self.parse_id(workspace) for workspace in workspaces
            ]
            query_builder.add_list_criteria("workspace", list_workspace_ids)
        # update the criteria with templates information
        if templates is not None and len(templates) > 0:
            list_template_ids = [
                self.parse_id(template) for template in templates
            ]
            query_builder.add_list_criteria("template", list_template_ids)
        # update the criteria with visibility information
        if options is not None and VISIBILITY_OPTION in options:
            query_builder.add_visibility_criteria(options[VISIBILITY_OPTION])
        # update the criteria with title information
        if title is not None:
            query_builder.add_title_criteria(title)

        # get raw query
        return query_builder.get_raw_query()

    def execute_raw_query(self, raw_query, order_by_field):
        """Execute the raw query in database

        Args:

            raw_query: Query to execute
            order_by_field:

        Returns:

            Results of the query
        """
        return data_api.execute_json_query(
            raw_query, self.request.user, order_by_field
        )

    @abstractmethod
    def build_response(self, data_list):
        """Build the paginated response.

        Args:

            data_list: List of data.

        Returns:

            The response
        """
        raise NotImplementedError("build_response method is not implemented.")

    @staticmethod
    def parse_id(obj):
        """Parse object id

        Args:
            obj:

        Returns:

        """
        if hasattr(obj, "id"):
            _id = obj.id
        elif isinstance(obj, dict) and "id" in obj:
            _id = obj["id"]
        else:
            raise RestApiError("Cannot find object id.")
        try:
            return int(_id)
        except (ValueError, TypeError):
            return _id


class AbstractMigrationView(APIView, metaclass=ABCMeta):
    """Abstract Migration View"""

    def post(self, request, template_id, migrate):
        """Retrieve all the Data and validate the associated
        Template and perform a migration if migrate = True

        Parameters:
            {
                "data": [
                    "data_id1",
                    "data_id2",
                    "data_id3"
                ],
                "xslt": "xslt_id"

            }

        Args:
            request: HTTP request
            template_id: Target template id
            migrate: (boolean) Perform the migration

        Returns:

            - code: 200
              content: Task id
            - code: 400
              content: Bad request
            - code: 403
              content: Forbidden
            - code: 500
              content: Internal server error
        """
        try:
            xslt_id = request.data["xslt"] if "xslt" in request.data else None
            if template_id and "data" in request.data:
                data_list = request.data["data"]
                # launch the migration task
                task_id = data_api.migrate_data_list(
                    data_list, xslt_id, template_id, migrate, request.user
                )
                return Response(task_id, status=status.HTTP_200_OK)
            elif template_id and "template" in request.data:
                data_list = request.data["template"]
                # launch the migration task
                task_id = data_api.migrate_template_list(
                    data_list, xslt_id, template_id, migrate, request.user
                )
                return Response(task_id, status=status.HTTP_200_OK)
            else:
                return Response(
                    "The target template id is not correct."
                    if not template_id
                    else "Please provide a template or data id to process.",
                    status.HTTP_400_BAD_REQUEST,
                )
        except AccessControlError as ace:
            return Response(str(ace), status.HTTP_403_FORBIDDEN)
        except Exception as exception:
            return Response(
                f"Wrong request, {str(exception)}",
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
