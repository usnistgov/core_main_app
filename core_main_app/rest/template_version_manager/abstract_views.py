""" REST abstract views for the template version manager API
"""
from abc import ABCMeta, abstractmethod

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.commons import exceptions as exceptions
from core_main_app.commons.exceptions import NotUniqueError, ApiError, XSDError
from core_main_app.components.template import api as template_api
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.rest.template_version_manager.serializers import TemplateVersionManagerSerializer, \
    CreateTemplateSerializer
from core_main_app.rest.template_version_manager.utils import can_user_modify_template_version_manager
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_main_app.utils.boolean import to_bool


class AbstractTemplateVersionManagerList(APIView):
    """ List template version managers.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_template_version_managers(self):
        """ Return template version managers.

        Returns:

        """
        raise NotImplementedError("get_template_version_managers method is not implemented.")

    def get(self, request):
        """ Get template version managers.

        Query Params:
            title: title
            is_disabled: [True|False]

        Args:
            request:

        Returns:

        """
        try:
            # Get objects
            object_list = self.get_template_version_managers()

            # Apply filters
            title = self.request.query_params.get('title', None)
            if title is not None:
                object_list = object_list.filter(title=title)

            is_disabled = self.request.query_params.get('is_disabled', None)
            if is_disabled is not None:
                object_list = object_list.filter(is_disabled=to_bool(is_disabled))

            # Serialize object
            serializer = TemplateVersionManagerSerializer(object_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AbstractStatusTemplateVersion(APIView):
    """
    Set template version status.
    """

    __metaclass__ = ABCMeta

    def get_object(self, pk):
        """ Get template from db

        Args:
            pk:

        Returns:

        """
        try:
            template_object = template_api.get(pk)
            template_version_manager_object = version_manager_api.get_from_version(template_object)
            can_user_modify_template_version_manager(template_version_manager_object, self.request.user)
            return template_object
        except exceptions.DoesNotExist:
            raise Http404

    @abstractmethod
    def status_update(self, template_object):
        """ Perform an update of the object status.

        Returns:

        """
        raise NotImplementedError("status_update method is not implemented.")

    def patch(self, request, pk):
        """ Set status.

        Args:
            request:

        Returns:

        """
        try:
            # Get object
            template_object = self.get_object(pk)

            # Set current template
            self.status_update(template_object)

            return Response(status=status.HTTP_200_OK)
        except Http404:
            content = {'message': 'Template not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as access_error:
            content = {'message': access_error.message}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ApiError as api_error:
            content = {'message': api_error.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AbstractTemplateVersionManagerDetail(APIView):
    """
    Template Version Manager Detail.
    """

    __metaclass__ = ABCMeta

    def get_object(self, pk):
        """ Get template version manager from db

        Args:
            pk:

        Returns:

        """
        try:
            template_version_manager_object = version_manager_api.get(pk)
            can_user_modify_template_version_manager(template_version_manager_object, self.request.user)
            return template_version_manager_object
        except exceptions.DoesNotExist:
            raise Http404


class AbstractStatusTemplateVersionManager(AbstractTemplateVersionManagerDetail):
    """
    Set template version manager status.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def status_update(self, template_version_manager_object):
        """ Perform an update of the object status.

        Returns:

        """
        raise NotImplementedError("status_update method is not implemented.")

    def patch(self, request, pk):
        """ Set status.

        Args:
            request:

        Returns:

        """
        try:
            # Get object
            template_version_manager_object = self.get_object(pk)

            # Set current template
            self.status_update(template_version_manager_object)

            return Response(status=status.HTTP_200_OK)
        except Http404:
            content = {'message': 'Template Version Manager not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as access_error:
            content = {'message': access_error.message}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AbstractTemplateList(APIView):
    """
    Create a template.
    """

    __metaclass__ = ABCMeta

    def post(self, request):
        """ Create a template.

        POST data
        {
        "title": "title",
        "filename": "filename",
        "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'/></xs:schema>"
        }

        Note: "dependencies"= json.dumps({"schemaLocation1": "id1" ,"schemaLocation2":"id2"})

        Args:
            request:

        Returns:

        """
        try:
            # Build serializers
            template_serializer = CreateTemplateSerializer(data=request.data)
            template_version_manager_serializer = TemplateVersionManagerSerializer(data=request.data)

            # Validate data
            template_serializer.is_valid(True)
            template_version_manager_serializer.is_valid(True)

            # Save data
            template_version_manager_object = template_version_manager_serializer.save(user=self.get_user())
            template_serializer.save(template_version_manager=template_version_manager_object)

            return Response(template_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except NotUniqueError:
            content = {'message': "A template with the same title already exists."}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except XSDError as xsd_error:
            content = {'message': "XSD Error: " + xsd_error.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @abstractmethod
    def get_user(self):
        raise NotImplementedError("get_user method is not implemented.")
