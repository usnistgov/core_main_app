""" REST views for the data API
"""
import json

from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.commons import exceptions
from core_main_app.components.data import api as data_api
from core_main_app.rest.data.abstract_views import AbstractExecuteLocalQueryView
from core_main_app.rest.data.serializers import DataSerializer, DataWithTemplateInfoSerializer
from core_main_app.utils.boolean import to_bool
from core_main_app.utils.databases.pymongo_database import get_full_text_query
from core_main_app.utils.file import get_file_http_response
from core_main_app.utils.pagination.rest_framework_paginator.pagination import StandardResultsSetPagination


# FIXME: permissions

class DataList(APIView):
    """ List all user data, or create a new one.
    """
    def get(self, request):
        """ Get all user data.

        Query Params:
            template: template id
            title: title

        Args:
            request:

        Returns:

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
        """ Create data

        Args:
            request:

        Returns:

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
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DataDetail(APIView):
    """
    Retrieve, update or delete a data.
    """
    def get_object(self, request, pk):
        """ Get data from db

        Args:
            request:
            pk:

        Returns:

        """
        try:
            return data_api.get_by_id(pk, request.user)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """ Retrieve data

        Args:
            request:
            pk:

        Returns:

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
        """ Delete a data

        Args:
            request:
            pk:

        Returns:

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
        """ Update data

        Args:
            request:
            pk:

        Returns:

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
    """
        Download XML file in data.
    """
    def get_object(self, request, pk):
        """ Get data from db

        Args:
            request:
            pk:

        Returns:

        """
        try:
            return data_api.get_by_id(pk, request.user)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """ Download data

        Args:
            request:
            pk:

        Returns:

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
# Should avoid here a duplication code with get_by_id
@api_view(['GET'])
def get_by_id_with_template_info(request):
    """ Get data by its id.

        /rest/data/get-full?id=588a73b47179c722f6fdaf43

        Args:
            request:

        Returns:

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
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExecuteLocalQueryView(AbstractExecuteLocalQueryView):
    def post(self, request):
        """ Execute a query.

        /rest/data/query/
        /rest/data/query/?page=2

        Example Data:
            {"query": "{\"root.element.value\": 2}"}
            {"query": "{\"root.element.value\": 2}", "all": "true"}
            {"query": "{\"root.element.value\": 2}", "templates": "[{\"id\":\"<template_id>\"}]"}
            {"query": "{}", "templates": "[{\"id\":\"<template_id>\"}]"}

        Args:
            request:

        Returns:

        """
        return super(ExecuteLocalQueryView, self).post(request)

    def build_response(self, data_list):
        """ Build the response.

        Args:
            data_list: List of data.

        Returns:
            The response.

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
    def build_query(self, query, templates):
        """ Build the raw query. Prepare the query for a keyword search.
        Args:
            query:
            templates:

        Returns:
            The raw query.

        """
        # build query builder
        query = json.dumps(get_full_text_query(query))
        return super(ExecuteLocalKeywordQueryView, self).build_query(str(query), templates)
