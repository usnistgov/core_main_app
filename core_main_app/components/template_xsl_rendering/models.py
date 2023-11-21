""" TemplateXslRendering model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.components.xsl_transformation.models import (
    XslTransformation,
)


class TemplateXslRendering(models.Model):
    """TemplateXslRendering object"""

    template = models.OneToOneField(
        Template, on_delete=models.CASCADE, blank=False
    )
    list_xslt = models.ForeignKey(
        XslTransformation,
        on_delete=models.SET_NULL,
        blank=True,
        related_name="list_xslt",
        null=True,
    )
    default_detail_xslt = models.ForeignKey(
        XslTransformation,
        on_delete=models.SET_NULL,
        blank=True,
        related_name="default_detail_xslt",
        null=True,
    )
    list_detail_xslt = models.ManyToManyField(
        XslTransformation,
        blank=True,
        default=[],
    )

    @staticmethod
    def get_by_id(template_xsl_rendering_id):
        """Get a TemplateXslRendering document by its id.

        Args:
            template_xsl_rendering_id: Id.

        Returns:
            TemplateXslRendering object.

        Raises:
            DoesNotExist: The TemplateXslRendering doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return TemplateXslRendering.objects.get(
                pk=template_xsl_rendering_id
            )
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_template_id(template_id):
        """Get TemplateXslRendering by its template id.

        Args:
            template_id: Template id.

        Returns:
            The TemplateXslRendering instance.

        Raises:
            DoesNotExist: The TemplateXslRendering doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return TemplateXslRendering.objects.get(template=template_id)
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_by_template_hash(template_hash):
        """Get TemplateXslRendering by its template hash.

        Args:
            template_hash: Template hash.

        Returns:
            The TemplateXslRendering instance.

        Raises:
            DoesNotExist: The TemplateXslRendering doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return TemplateXslRendering.objects.get(
                template___hash=template_hash
            )
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_all():
        """Get all TemplateXslRendering.

        Returns:
            List of TemplateXslRendering.

        """
        return TemplateXslRendering.objects.all()

    def __str__(self):
        """Template Xsl Rendering as string

        Returns:

        """
        return str(self.template)
