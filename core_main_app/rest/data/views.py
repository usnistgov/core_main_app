""" REST views for the data API
"""
import json

from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.commons import exceptions
from core_main_app.components.data import api as data_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.rest.data.abstract_views import AbstractExecuteLocalQueryView
from core_main_app.rest.data.serializers import DataSerializer, DataWithTemplateInfoSerializer
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_main_app.utils.boolean import to_bool
from core_main_app.utils.databases.pymongo_database import get_full_text_query
from core_main_app.utils.file import get_file_http_response
from core_main_app.utils.pagination.rest_framework_paginator.pagination import StandardResultsSetPagination


class DataList(APIView):
    """ List all user Data, or create a new one.
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """ Get all user Data

        Url Parameters:

            template: template_id
            title: document_title

        Examples:

            ../data/
            ../data?template=[template_id]
            ../data?title=[document_title]
            ../data?template=[template_id]&title=[document_title]

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
            template = self.request.query_params.get('template', None)
            if template is not None:
                data_object_list = data_object_list.filter(template=template)

            title = self.request.query_params.get('title', None)
            if title is not None:
                data_object_list = data_object_list.filter(title=title)

            # Serialize object
            data_serializer = DataSerializer(data_object_list, many=True)

            # Return response
            return Response(data_serializer.data, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """ Create a Data

        Parameters:

            {
                "title": "document_title",
                "template": "template_id",
                "xml_content": "document_content"
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
            data_serializer = DataSerializer(data=request.data)

            # Validate data
            data_serializer.is_valid(True)
            # Save data
            data_serializer.save(user=request.user)

            # Return the serialized data
            return Response(data_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.DoesNotExist:
            content = {'message': 'Template not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DataDetail(APIView):
    """ Retrieve, update or delete a Data
    """
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_object(self, request, pk):
        """ Get data from db

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
        """ Retrieve a data

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
            # Get object
            data_object = self.get_object(request, pk)

            # Serialize object
            serializer = DataSerializer(data_object)

            # Return response
            return Response(serializer.data)
        except Http404:
            content = {'message': 'Data not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """ Delete a Data

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
            content = {'message': 'Data not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        """ Update a Data

        Parameters:

            {
                "title": "new_title",
                "xml_content": "new_xml_content"
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
            data_serializer = DataSerializer(instance=data_object,
                                             data=request.data,
                                             partial=True)

            # Validate data
            data_serializer.is_valid(True)
            # Save data
            data_serializer.save(user=request.user)

            return Response(data_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            content = {'message': 'Data not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DataDownload(APIView):
    """ Download XML file in data
    """
    def get_object(self, request, pk):
        """ Get Data from db

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
        """ Download the XML file from a data

        Args:

            request: HTTP request
            pk: ObjectId

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

            return get_file_http_response(data_object.xml_content, data_object.title, 'text/xml', 'xml')
        except Http404:
            content = {'message': 'Data not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# FIXME: Should use in the future an serializer with dynamic fields (init depth with parameter for example)
# FIXME: Should avoid the duplicated code with get_by_id
@api_view(['GET'])
def get_by_id_with_template_info(request):
    """ Retrieve a Data with template information

    Examples:

        ../data/get-full?id=[data_id]

    Args:

        request: HTTP request

    Returns:

        - code: 200
          content: Data
        - code: 400
          content: Validation error
        - code: 404
          content: Object was not found
        - code: 500
          content: Internal server error
    """
    try:
        # Get parameters
        data_id = request.query_params.get('id', None)

        # Check parameters
        if data_id is None:
            content = {'message': 'Expected parameters not provided.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Get object
        data_object = data_api.get_by_id(data_id, request.user)

        # Serialize object
        return_value = DataWithTemplateInfoSerializer(data_object)

        # Return response
        return Response(return_value.data, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist as e:
        content = {'message': 'No data found with the given id.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions.ModelError:
        content = {'message': 'Invalid input.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        content = {'message': 'An unexpected error occurred.'}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExecuteLocalQueryView(AbstractExecuteLocalQueryView):
    def post(self, request):
        """ Execute a query

        Url Parameters:

            page: page_number

        Parameters:

            # get all results (paginated)
            {"query": "{}"}
            # get all results
            {"query": "{}", "all": "true"}
            # get all results filtered by title
            {"query": "{}", "title": "title_string"}
            # get all results filtered by templates
            {"query": "{}", "templates": "[{\\"id\\":\\"[template_id]\\"}]"}
            # get all results that verify a given criteria
            {"query": "{\\"root.element.value\\": 2}"}
            # get results using multiple options
            {"query": "{\\"root.element.value\\": 2}", "templates": "[{\\"id\\":\\"template_id\\"}]", "all": "true"}

        Warning:

            Need to backslash double quotes in JSON payload

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
        return super(ExecuteLocalQueryView, self).post(request)

    def build_response(self, data_list):
        """ Build the response.

        Args:

            data_list: List of data

        Returns:

            The response paginated
        """
        if 'all' in self.request.data and to_bool(self.request.data['all']):
            # Serialize data list
            data_serializer = DataSerializer(data_list, many=True)
            # Return response
            return Response(data_serializer.data)
        else:
            # Get paginator
            paginator = StandardResultsSetPagination()

            # Get requested page from list of results
            page = paginator.paginate_queryset(data_list, self.request)

            # Serialize page
            data_serializer = DataSerializer(page, many=True)

            # Return paginated response
            return paginator.get_paginated_response(data_serializer.data)


class ExecuteLocalKeywordQueryView(ExecuteLocalQueryView):
    def build_query(self, query, templates, options, title=None):
        """ Build the raw query
        Prepare the query for a keyword search

        Args:

            query: ObjectId
            templates: ObjectId
            options: Query options
            title: title filter
            
        Returns:

            The raw query
        """
        # build query builder
        query = json.dumps(get_full_text_query(query))
        return super(ExecuteLocalKeywordQueryView, self).build_query(str(query), templates, options, title)


class DataAssign(APIView):
    """ Assign a Data to a Workspace.
    """
    def get_object(self, request, pk):
        """ Get data from db

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
        """ Retrieve a Workspace

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
        """ Assign Data to a Workspace

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
            content = {'message': 'Data or workspace not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as ace:
            content = {'message': ace.message}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
