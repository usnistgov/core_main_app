""" REST views for the data API
"""
from rest_framework.decorators import api_view
from core_main_app.components.template import api as template_api
from rest_framework.response import Response
from rest_framework import status

from core_main_app.commons import exceptions
from core_main_app.rest.data.serializers import CreateDataSerializer, DataSerializer
import core_main_app.components.data.api as data_api
import json


@api_view(['GET', 'POST'])
def data(request):
    """ Data rest api

    Args:
        request:

    Returns:

    """
    if request.method == 'GET':
        return get_all(request)
    elif request.method == 'POST':
        return post(request)


@api_view(['GET'])
def get_all(request):
    """

    Args:
        request:

    Returns:

    """
    try:
        # Get object
        data_object_list = data_api.get_all()

        # Serialize object
        return_value = DataSerializer(data_object_list, many=True)

        # Return response
        return Response(return_value.data, status=status.HTTP_200_OK)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_by_id(request):
    """ Get json Data

        /rest/data/get?id=588a73b47179c722f6fdaf43

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
        data_object = data_api.get_by_id(data_id)

        # Serialize object
        return_value = DataSerializer(data_object)

        # Return response
        return Response(return_value.data, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist as e:
        content = {'message': 'No data found with the given id.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def post(request):
    """ POST /rest/data
    {
        "template": "588a728a7179c72131ec11ae",
        "user_id": "1",
        "title": "title",
        "xml_file": "<root>1</root>"
    }

    Args:
        request:

    Returns:

    """
    try:
        # Build serializer
        data_serializer = CreateDataSerializer(data=request.data)

        # Validate data
        data_serializer.is_valid(True)

        # Deserialize object
        data = data_serializer.create(data_serializer.data)
        data.template = template_api.get(request.data['template'])

        # Upsert the data
        data_api.upsert(data)

        # Returns the serialized template
        return_value = DataSerializer(data)

        return Response(return_value.data, status=status.HTTP_201_CREATED)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def execute_query(request):
    """ POST /rest/data/query
    {
        "query": "{\"dict_content.root.element.value\": 1}",
    }

    Args:
        request:

    Returns:

    """
    try:
        query = request.data.get('query', None)
        if query is None:
            content = {'message': 'Expected parameters not provided.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            json_query = json.loads(query)
        except:
            content = {'message': 'Query format is not correct.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Executes query
        data_object_list = data_api.execute_query(json_query)

        # Serialize object
        return_value = DataSerializer(data_object_list, many=True)

        # Return response
        return Response(return_value.data, status=status.HTTP_200_OK)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
