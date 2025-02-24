""" REST views for the data API
"""

import json
import logging

from django.conf import settings as conf_settings
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.access_control.api import check_can_write
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import XMLError
from core_main_app.components.data import api as data_api
from core_main_app.components.data import tasks as data_tasks
from core_main_app.components.template.models import Template
from core_main_app.components.user import api as user_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.rest.data.abstract_views import (
    AbstractExecuteLocalQueryView,
)
from core_main_app.rest.data.abstract_views import AbstractMigrationView
from core_main_app.rest.data.admin_serializers import AdminDataSerializer
from core_main_app.rest.data.serializers import (
    DataSerializer,
    DataWithTemplateInfoSerializer,
)
from core_main_app.rest.mongo_data.serializers import MongoDataSerializer
from core_main_app.rest.template_html_rendering.views import BaseDataHtmlRender
from core_main_app.settings import MAX_DOCUMENT_LIST
from core_main_app.utils.boolean import to_bool
from core_main_app.utils.databases.mongo.pymongo_database import (
    get_full_text_query,
)
from core_main_app.utils.file import (
    get_file_http_response,
    get_data_file_content_type_for_template_format,
    get_data_file_extension_for_template_format,
)
from core_main_app.utils.json_utils import (
    format_content_json,
)
from core_main_app.utils.pagination.rest_framework_paginator.pagination import (
    StandardResultsSetPagination,
)
from core_main_app.utils.xml import get_content_by_xpath, format_content_xml

logger = logging.getLogger(__name__)


class DataList(APIView):
    """List all user Data, or create a new one."""

    permission_classes = (IsAuthenticated,)
    serializer = DataSerializer

    def get(self, request):
        """Get all user Data

        Url Parameters:

            workspace: workspace_id
            template: template_id
            title: document_title
            regex: true|false

        Examples:

            ../data/
            ../data?page=2
            ../data?workspace=[workspace_id]
            ../data?template=[template_id]
            ../data?title=[document_title]
            ../data?title=[document_title]&regex=true
            ../data?template=[template_id]&title=[document_title]&page=3

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: List of data
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            data_object_list = data_api.get_all_by_user(request.user)

            # Apply filters
            workspace = self.request.query_params.get("workspace", None)
            if workspace is not None:
                data_object_list = data_object_list.filter(workspace=workspace)

            template = self.request.query_params.get("template", None)
            if template is not None:
                data_object_list = data_object_list.filter(template=template)

            title = self.request.query_params.get("title", None)

            if title is not None:
                regex = self.request.query_params.get("regex", False)
                title_filter = (
                    {"title__iregex": title}
                    if to_bool(regex)
                    else {"title": title}
                )
                data_object_list = data_object_list.filter(**title_filter)

            # Get paginator
            paginator = StandardResultsSetPagination()

            # Get requested page from list of results
            page = paginator.paginate_queryset(data_object_list, self.request)

            # Serialize page
            data_serializer = self.serializer(page, many=True)

            # Return paginated response
            return paginator.get_paginated_response(data_serializer.data)

        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """Create a Data

        Parameters:

            {
                "title": "document_title",
                "template": "template_id",
                "workspace": "workspace_id",
                "content": "document_content"
            }

        Args:

            request: HTTP request

        Returns:

            - code: 201
              content: Created data
            - code: 400
              content: Validation error
            - code: 404
              content: Template was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Build serializer
            data_serializer = self.serializer(
                data=request.data, context={"request": request}
            )

            # Validate data
            data_serializer.is_valid(raise_exception=True)
            # Save data
            data_serializer.save()

            # Return the serialized data
            return Response(
                data_serializer.data, status=status.HTTP_201_CREATED
            )
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.DoesNotExist:
            content = {"message": "Template not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminDataList(DataList):
    """Admin Data List"""

    permission_classes = (IsAdminUser,)
    serializer = AdminDataSerializer

    def get(self, request):
        """Get all Data

        Url Parameters:

            user: user_id
            workspace: workspace_id
            template: template_id
            title: document_title
            regex: true|false

        Examples:

            ../data/
            ../data?user=[user_id]
            ../data?workspace=[workspace_id]
            ../data?template=[template_id]
            ../data?title=[document_title]
            ../data?title=[document_title]&regex=true
            ../data?template=[template_id]&title=[document_title]

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: List of data
            - code: 500
              content: Internal server error
        """
        if not request.user.is_superuser:
            content = {"message": "Only a superuser can use this feature."}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        try:
            # Get object
            data_object_list = data_api.get_all(request.user)

            # Apply filters
            user = self.request.query_params.get("user", None)
            if user is not None:
                data_object_list = data_object_list.filter(user_id=user)

            workspace = self.request.query_params.get("workspace", None)
            if workspace is not None:
                data_object_list = data_object_list.filter(workspace=workspace)

            template = self.request.query_params.get("template", None)
            if template is not None:
                data_object_list = data_object_list.filter(template=template)

            title = self.request.query_params.get("title", None)

            if title is not None:
                regex = self.request.query_params.get("regex", False)
                title_filter = (
                    {"title__iregex": title}
                    if to_bool(regex)
                    else {"title": title}
                )
                data_object_list = data_object_list.filter(**title_filter)

            # Serialize object
            data_serializer = self.serializer(data_object_list, many=True)

            # Return response
            return Response(data_serializer.data, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        if not request.user.is_superuser:
            content = {"message": "Only a superuser can use this feature."}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        return super().post(request)


class DataDetail(APIView):
    """Retrieve, update or delete a Data"""

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer = DataSerializer

    def get_object(self, request, pk):
        """Get data from db

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            Data
        """
        try:
            return data_api.get_by_id(pk, request.user)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """Retrieve a data

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: Data
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get parameters
            template_info_param = to_bool(
                self.request.query_params.get("template_info", False)
            )
            if template_info_param:
                self.serializer = DataWithTemplateInfoSerializer

            # Get object
            data_object = self.get_object(request, pk)

            # Serialize object
            serializer = self.serializer(data_object)

            # Return response
            return Response(serializer.data)
        except Http404:
            content = {"message": "Data not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        """Delete a Data

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 204
              content: Deletion succeed
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            data_object = self.get_object(request, pk)

            # delete object
            data_api.delete(data_object, request.user)

            # Return response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            content = {"message": "Data not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        """Update a Data

        Parameters:

            {
                "title": "new_title",
                "content": "new_xml_content"
            }

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: Updated data
            - code: 400
              content: Validation error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            data_object = self.get_object(request, pk)

            # Build serializer
            data_serializer = self.serializer(
                instance=data_object,
                data=request.data,
                partial=True,
                context={"request": request},
            )

            # Validate data
            data_serializer.is_valid(raise_exception=True)
            # Save data
            data_serializer.save()

            return Response(data_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            content = {"message": "Data not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DataChangeOwner(APIView):
    """Change the Owner of a data"""

    permission_classes = (IsAdminUser,)

    def get_object(self, request, pk):
        """Get data from db

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            Data
        """
        try:
            return data_api.get_by_id(pk, request.user)
        except exceptions.DoesNotExist:
            raise Http404

    def get_user(self, user_id):
        """Retrieve a User

        Args:

            user_id: ObjectId

        Returns:

            - code: 404
              content: Object was not found
        """
        try:
            return user_api.get_user_by_id(user_id)
        except exceptions.DoesNotExist:
            raise Http404

    def patch(self, request, pk, user_id):
        """Change the Owner of a data

        Args:

            request: HTTP request
            pk: ObjectId
            user_id: ObjectId

        Returns:

            - code: 200
              content: None
            - code: 403
              content: Authentication error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # get object
            data_object = self.get_object(request, pk)
            user_object = self.get_user(user_id)

            # change owner
            data_api.change_owner(data_object, user_object, request.user)
            return Response({}, status=status.HTTP_200_OK)
        except Http404:
            content = {"message": "Data or user not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as ace:
            content = {"message": str(ace)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DataDownload(APIView):
    """Download XML file in data"""

    def get_object(self, request, pk):
        """Get Data from db

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            Data
        """
        try:
            return data_api.get_by_id(pk, request.user)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """Download the XML file from a data

        Args:

            request: HTTP request
            pk: ObjectId

        Examples:

            ../data/download/[data_id]
            ../data/download/[data_id]?pretty_print=true

        Returns:

            - code: 200
              content: XML file
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            data_object = self.get_object(request, pk)

            # get xml content
            data_content = data_object.content

            # get format bool
            pretty_print = request.query_params.get("pretty_print", False)

            # format content
            if to_bool(pretty_print):
                # format XML
                if data_object.template.format == Template.XSD:
                    data_content = format_content_xml(data_content)
                # format JSON
                elif data_object.template.format == Template.JSON:
                    data_content = format_content_json(data_content)
                else:
                    content = {"message": "Unsupported format."}
                    return Response(
                        content, status=status.HTTP_400_BAD_REQUEST
                    )

            return get_file_http_response(
                data_content,
                data_object.title,
                content_type=get_data_file_content_type_for_template_format(
                    data_object.template.format
                ),
                extension=get_data_file_extension_for_template_format(
                    data_object.template.format
                ),
            )
        except Http404:
            content = {"message": "Data not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except XMLError:
            content = {"message": "Content is not well formatted XML."}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExecuteLocalQueryView(AbstractExecuteLocalQueryView):
    """Execute Local Query View"""

    if conf_settings.MONGODB_INDEXING:
        serializer = MongoDataSerializer
    else:
        serializer = DataSerializer

    def post(self, request):
        """Execute a query

        Url Parameters:

            page: page_number

        Parameters:

            # get all results (paginated)
            {"query": {}}
            # get all results
            {"query": {}, "all": "true"}
            # get all results filtered by title
            {"query": {}, "title": "title_string"}
             # get all results filtered by workspaces
            {"query": {}, "workspaces": [{"id":"[workspace_id]"}]}
            # get all results filtered by private workspace
            {"query": {}, "workspaces": [{"id":"None"}]}
            # get all results filtered by templates
            {"query": {}, "templates": [{"id":"[template_id]"}] }
            # get all results that verify a given criteria
            {"query": {"root.element.value": 2}}
            # get values at xpath
            {"query": {}, "xpath": "/ns:root/@element", "namespaces": {"ns": "<namespace_url>"}}
            # get results using multiple options
            {"query": {"root.element.value": 2}, "workspaces": [{"id":"workspace_id"}] , "all": "true"}
            {"query": {"root.element.value": 2}, "templates": [{"id":"template_id"}] , "all": "true"}
            {"query": {"root.element.value": 2}, "templates": [{"id":"template_id"}],
            "workspaces": [{"id":"[workspace_id]"}] ,"all": "true"}

        Examples:

            ../data/query/
            ../data/query/?page=2

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: List of data
            - code: 400
              content: Bad request
            - code: 500
              content: Internal server error
        """
        return super().post(request)

    def build_response(self, data_list):
        """Build the response.

        Args:

            data_list: List of data

        Returns:

            The response paginated
        """

        xpath = self.request.data.get("xpath", None)
        namespaces = self.request.data.get("namespaces", None)
        if "all" in self.request.data and to_bool(self.request.data["all"]):
            if data_list.count() > MAX_DOCUMENT_LIST:
                content = {"message": "Number of documents is over the limit."}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            # Select values at xpath if provided
            if xpath:
                for data_object in data_list:
                    data_object.xml_content = get_content_by_xpath(
                        data_object.xml_content, xpath, namespaces=namespaces
                    )
            # Serialize data list
            data_serializer = self.serializer(data_list, many=True)
            # Return response
            return Response(data_serializer.data)
        else:
            # Get paginator
            paginator = StandardResultsSetPagination()

            # Get requested page from list of results
            page = paginator.paginate_queryset(data_list, self.request)

            # Select values at xpath if provided
            if xpath:
                for data_object in page:
                    data_object.xml_content = get_content_by_xpath(
                        data_object.xml_content, xpath, namespaces=namespaces
                    )

            # Serialize page
            data_serializer = self.serializer(page, many=True)

            # Return paginated response
            return paginator.get_paginated_response(data_serializer.data)


class ExecuteLocalKeywordQueryView(ExecuteLocalQueryView):
    """Execute Local Keyword Query View"""

    def build_query(
        self, query, workspaces=None, templates=None, options=None, title=None
    ):
        """Build the raw query
        Prepare the query for a keyword search

        Args:

            query: ObjectId
            workspaces: ObjectId
            templates: ObjectId
            options: Query options
            title: title filter

        Returns:

            The raw query
        """
        # build query builder
        query = json.dumps(get_full_text_query(query))
        return super().build_query(
            query=str(query),
            workspaces=workspaces,
            templates=templates,
            options=options,
            title=title,
        )


class DataAssign(APIView):
    """Assign a Data to a Workspace."""

    permission_classes = (IsAuthenticated,)

    def get_object(self, request, pk):
        """Get data from db

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            Data
        """
        try:
            return data_api.get_by_id(pk, request.user)
        except exceptions.DoesNotExist:
            raise Http404

    def get_workspace(self, workspace_id):
        """Retrieve a Workspace

        Args:

            workspace_id: ObjectId

        Returns:

            - code: 404
              content: Object was not found
        """
        try:
            return workspace_api.get_by_id(workspace_id)
        except exceptions.DoesNotExist:
            raise Http404

    def patch(self, request, pk, workspace_id):
        """Assign Data to a Workspace

        Args:

            request: HTTP request
            pk: ObjectId
            workspace_id: ObjectId

        Returns:

            - code: 200
              content: None
            - code: 403
              content: Authentication error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            data_object = self.get_object(request, pk)
            workspace_object = self.get_workspace(workspace_id)

            # Assign data to workspace
            data_api.assign(data_object, workspace_object, request.user)
            return Response({}, status=status.HTTP_200_OK)
        except Http404:
            content = {"message": "Data or workspace not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as ace:
            content = {"message": str(ace)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DataListByWorkspace(APIView):
    """List all Data by workspace."""

    permission_classes = (IsAuthenticated,)
    serializer = DataSerializer

    def get(self, request, workspace_id):
        """Get all workspace Data

        Examples:

            ../workspace/id/data


        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: List of data
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            data_object_list = data_api.get_all_by_workspace(
                workspace_id, request.user
            )

            # Serialize object
            data_serializer = self.serializer(data_object_list, many=True)

            # Return response
            return Response(data_serializer.data, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DataPermissions(APIView):
    """
    Get the permissions of the data according to the client user
    """

    def get(self, request):
        """GET requests"""
        return self.process_request(request)

    def post(self, request):
        """POST requests"""
        return self.process_request(request)

    def get_object(self, request, pk):
        """Get data from db

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            Data
        """
        try:
            return data_api.get_by_id(pk, request.user)
        except exceptions.DoesNotExist:
            raise Http404

    def process_request(self, request):
        """Give the user permissions for a list of data ids

        Parameters:

            [
                "data_id1"
                "data_id2"
                "data_id3"
                ...
            ]

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: JSON Array [ <data_id>: <boolean> ]
            - code: 400
              content: Validation error
            - code: 404
              content: Template was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Build serializer
            data_ids = json.loads(request.query_params["ids"])
            results = {}

            for id in data_ids:
                results[id] = self.can_write_data(request, id)

            return Response(results, status.HTTP_200_OK)

        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            content = {"message": "Data not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def can_write_data(self, request, id):
        """Get the data permissions of a data

        Args:

            request: http request
            id: data id

        Returns:

            - Boolean
            - raise: Http404
              content: Data was not found
            - raise: Exception
              content: Unknown error
        """
        try:
            # Get object
            data_object = self.get_object(request, id)
            check_can_write(data_object, request.user)
            return True
        except AccessControlError:
            return False
        except Exception as exception:
            raise exception


class Validation(AbstractMigrationView):
    """Check for a set of data if the migration is possible for the given target template"""

    def post(self, request, pk):
        """Check if a migration if possible for the given template id

        Parameters:

            {
                "data || template": [
                    "id1",
                    "id2",
                    "id3"
                ]
            }

        Args:

            request: HTTP request
            pk: Target template id

        Returns:

            - code: 200
              content: Migration done
            - code: 400
              content: Bad request
            - code: 403
              content: Access denied
            - code: 500
              content: Internal server error
        """
        return super().post(request=request, template_id=pk, migrate=False)


class Migration(AbstractMigrationView):
    """Data template migration"""

    def post(self, request, pk):
        """Migrate data to the given template id

        Parameters:

            {
                "data || template": [
                    "id1",
                    "id2",
                    "id3"
                ]
            }

        Args:

            request: HTTP request
            pk: Target template id

        Returns:

            - code: 200
              content: Migration done
            - code: 400
              content: Bad request
            - code: 403
              content: Access denied
            - code: 500
              content: Internal server error
        """
        return super().post(request=request, template_id=pk, migrate=True)


class GetTaskProgress(APIView):
    """Get the progress of the migration / validation async task"""

    permission_classes = (IsAdminUser,)

    def get(self, request, task_id):
        """Get the progress of the migration / validation async task

        Args:
            request:
            task_id:

        Return:
            {
                'state': PENDING | PROGRESS | SUCCESS,
                'details': result (for SUCCESS) | null (for PENDING) | { PROGRESS info }
            }
        """
        result = data_tasks.get_task_progress(task_id)
        return Response(result, content_type="application/json")


class GetTaskResult(APIView):
    """Get the result of the migration / validation async task"""

    permission_classes = (IsAdminUser,)

    def get(self, request, task_id):
        """Get the result of the migration / validation async task

        Args:
            request:
            task_id:

        Return:
            {
                    "valid": ["data_id_1", "data_id_2" ...],
                    "wrong": ["data_id_3", "data_id_4" ...]
            }
        """
        result = data_tasks.get_task_result(task_id)
        return Response(result, content_type="application/json")


class DataHtmlRender(BaseDataHtmlRender):
    """Data Html Render"""

    def get_object(self, pk, request):
        """get data by id."""
        return data_api.get_by_id(pk, request.user)

    def get(self, request, pk):
        """Get Html render

        Args:
            request: HTTP request
            pk: data id

        Parameters:

            {
                "rendering": "list/detail"
            }

        Returns:
            Html string
        """

        # Get rendering content
        return self.get_rendering_content(request, pk)
