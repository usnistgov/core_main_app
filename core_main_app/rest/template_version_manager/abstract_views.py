""" REST abstract views for the template version manager API
"""
from abc import ABCMeta, abstractmethod

from django.http import Http404
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions as exceptions
from core_main_app.commons.exceptions import NotUniqueError, ApiError, XSDError
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.rest.template_version_manager.serializers import (
    TemplateVersionManagerSerializer,
    CreateTemplateSerializer,
    TemplateVersionManagerOrderingSerializer,
)
from core_main_app.utils.boolean import to_bool
from core_main_app.utils.decorators import api_staff_member_required


class AbstractTemplateVersionManagerList(APIView, metaclass=ABCMeta):
    """List template version managers"""

    serializer = TemplateVersionManagerSerializer

    @abstractmethod
    def get_template_version_managers(self):
        """Return template version managers"""
        raise NotImplementedError(
            "get_template_version_managers method is not implemented."
        )

    def get(self, request):
        """Get template version managers

        Url Parameters:

            template: template_id
            title: document_title

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: List of template version manager
            - code: 500
              content: Internal server error
        """
        try:
            # Get objects
            object_list = self.get_template_version_managers()

            # Apply filters
            title = self.request.query_params.get("title", None)
            if title is not None:
                object_list = object_list.filter(title=title)

            is_disabled = self.request.query_params.get("is_disabled", None)
            if is_disabled is not None:
                object_list = object_list.filter(
                    is_disabled=to_bool(is_disabled)
                )

            # Serialize object
            serializer = self.serializer(object_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AccessControlError:
            content = {"message": "Access Forbidden"}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AbstractStatusTemplateVersion(APIView, metaclass=ABCMeta):
    """Set template version status"""

    def get_object(self, pk, request):
        """Get template from db

        Args:

            pk: ObjectId
            request:

        Returns:

            Template
        """
        try:
            template_object = template_api.get_by_id(pk, request=request)
            return template_object
        except exceptions.DoesNotExist:
            raise Http404

    @abstractmethod
    def status_update(self, template_object):
        """Perform an update of the object status"""
        raise NotImplementedError("status_update method is not implemented.")

    @method_decorator(api_staff_member_required())
    def patch(self, request, pk):
        """Set status

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: None
            - code: 400
              content: Validation error / bad request
            - code: 403
              content: Authentication error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            template_object = self.get_object(pk, request=request)

            # Set current template
            self.status_update(template_object)

            return Response(status=status.HTTP_200_OK)
        except Http404:
            content = {"message": "Template not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as access_error:
            content = {"message": str(access_error)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ApiError as api_error:
            content = {"message": str(api_error)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AbstractTemplateVersionManagerDetail(APIView, metaclass=ABCMeta):
    """Template Version Manager Detail"""

    def get_object(self, pk):
        """Get template version manager from db

        Args:

            pk: ObjectId

        Returns:

            TemplateVersionManager
        """
        try:
            template_version_manager_object = (
                template_version_manager_api.get_by_id(
                    pk, request=self.request
                )
            )
            return template_version_manager_object
        except exceptions.DoesNotExist:
            raise Http404


class AbstractStatusTemplateVersionManager(
    AbstractTemplateVersionManagerDetail, metaclass=ABCMeta
):
    """Set template version manager status"""

    @abstractmethod
    def status_update(self, template_version_manager_object):
        """Perform an update of the object status."""
        raise NotImplementedError("status_update method is not implemented.")

    def patch(self, request, pk):
        """Set status

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: None
            - code: 400
              content: Validation error
            - code: 403
              content: Authentication error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            template_version_manager_object = self.get_object(pk)

            # Set current template
            self.status_update(template_version_manager_object)

            return Response(status=status.HTTP_200_OK)
        except Http404:
            content = {"message": "Template Version Manager not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as access_error:
            content = {"message": str(access_error)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AbstractTemplateList(APIView, metaclass=ABCMeta):
    """Create a template"""

    serializer = TemplateVersionManagerSerializer
    create_serializer = CreateTemplateSerializer

    def post(self, request):
        """Create a template

        Parameters:

            {
                "title": "title",
                "filename": "filename",
                "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'/></xs:schema>"
            }

        Note:

            "dependencies_dict": json.dumps({"schemaLocation1": "id1" ,"schemaLocation2":"id2"})

        Args:

            request: HTTP request

        Returns:

            - code: 201
              content: Created template
            - code: 400
              content: Validation error / not unique / XSD error
            - code: 500
              content: Internal server error
        """
        try:
            # Build serializers
            template_serializer = self.create_serializer(
                data=request.data, context={"request": request}
            )
            template_version_manager_serializer = self.serializer(
                data=request.data
            )

            # Validate data
            template_serializer.is_valid(raise_exception=True)
            template_version_manager_serializer.is_valid(raise_exception=True)

            # Save data
            template_version_manager_object = (
                template_version_manager_serializer.save(user=self.get_user())
            )
            template_serializer.save(
                template_version_manager=template_version_manager_object,
                user=self.get_user(),
            )

            return Response(
                template_serializer.data, status=status.HTTP_201_CREATED
            )
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except NotUniqueError:
            content = {
                "message": "A template with the same title already exists."
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except XSDError as xsd_error:
            content = {"message": "XSD Error: " + str(xsd_error)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @abstractmethod
    def get_user(self):
        """Retrieve a user"""
        raise NotImplementedError("get_user method is not implemented.")


class AbstractOrderingTemplateVersionManager(APIView, metaclass=ABCMeta):
    """Set template version manager rank"""

    serializer = TemplateVersionManagerOrderingSerializer
    permission_classes = (IsAuthenticated,)

    @abstractmethod
    def get_objects(self):
        """get template version manager list."""
        raise NotImplementedError("get_objects method is not implemented.")

    @abstractmethod
    def update_ordering(self, list_ids):
        """update TemplateVersionManager ordering

        Args:
            list_ids:
        Returns:

        """
        raise NotImplementedError("update_ordering method is not implemented.")

    def get(self, request):
        """Get template version managers

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: List of template version manager
            - code: 403
              content: Access control error
            - code: 404
              content: template(s) Not found
            - code: 500
              content: Internal server error
        """
        try:
            object_list = self.get_objects()

            # Serialize object
            serializer = self.serializer(object_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request):
        """Update templates ordering


        Parameters:

            {
                "template_list" : [template_version_manager1_id, template_version_manager2_id]
            }

        Example:

            "template_list": [2, 19, 3, 1]

        Args:

            request: HTTP request

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
            # get list ids
            template_ids = request.data.get("template_list", [])

            # check duplicate ids
            if len(template_ids) != len(set(template_ids)):
                content = {
                    "message": "Action not processed due to duplicate ids."
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            # update template ordering
            self.update_ordering(template_ids)

            # Serialize objects
            serializer = self.serializer(self.get_objects(), many=True)

            # return response
            return Response(serializer.data, status=status.HTTP_200_OK)

        except AccessControlError as ace:
            content = {"message": str(ace)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except exceptions.DoesNotExist as dne:
            content = {"message": str(dne)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
