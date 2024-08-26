""" TemplateHtmlRendering model
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template


class TemplateHtmlRendering(models.Model):
    """TemplateHtmlRendering object"""

    template = models.OneToOneField(
        Template, on_delete=models.CASCADE, blank=False
    )
    list_rendering = models.TextField(blank=True)
    detail_rendering = models.TextField(blank=True)

    @staticmethod
    def get_all():
        """Return all TemplateHtmlRendering.

        Returns:
            list<TemplateHtmlRendering> .
        """

        return TemplateHtmlRendering.objects.all()

    @staticmethod
    def get_by_id(template_html_rendering_id):
        """Return a template by its id.

        Args:
            template_html_rendering_id:

        Returns:

        """
        try:
            return TemplateHtmlRendering.objects.get(
                pk=template_html_rendering_id
            )
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_by_template_id(template_id):
        """Get TemplateHtmlRendering by its template id.

        Args:
            template_id: Template id.

        Returns:
            The TemplateHtmlRendering instance.

        Raises:
            DoesNotExist: The TemplateHtmlRendering doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return TemplateHtmlRendering.objects.get(template=template_id)
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_by_template_hash(template_hash):
        """Get TemplateHtmlRendering by its template hash.

        Args:
            template_hash: Template hash.

        Returns:
            The TemplateHtmlRendering instance.

        Raises:
            DoesNotExist: The TemplateHtmlRendering doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return TemplateHtmlRendering.objects.get(
                template___hash=template_hash
            )
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    def __str__(self):
        """Template Html Rendering as string

        Returns:

        """
        return str(self.template)
