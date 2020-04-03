""" TemplateXslRendering API calls
"""
import logging

from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import ApiError
from core_main_app.components.template import api as template_api
from core_main_app.components.template_xsl_rendering.models import TemplateXslRendering

logger = logging.getLogger(__name__)


def add_or_delete(template_id, list_xslt, detail_xslt, template_xsl_rendering_id=None):
    """ Manage the saving of a TemplateXslRendering. If no XSLTs have been given,
    deletes the instance.

    Args:
        template_id: TemplateXslRendering.
        list_xslt: XSLT.
        detail_xslt: XSLT.
        template_xsl_rendering_id: Instance id.

    Returns:

    """
    # Boolean to know if we need this instance in database, i.e there are XSLTs information.
    need_to_be_kept = list_xslt is not None or detail_xslt is not None

    if need_to_be_kept:
        return upsert(template_id, list_xslt, detail_xslt, template_xsl_rendering_id)
    else:
        try:
            if template_xsl_rendering_id:
                template_xsl_rendering = get_by_id(template_xsl_rendering_id)
                delete(template_xsl_rendering)

            return None
        except Exception:
            raise ApiError("An error occured while deleting the TemplateXSLRendering")


def upsert(template_id, list_xslt, detail_xslt, template_xsl_rendering_id=None):
    """ Update or create a XSL Template rendering object

    Args:
        template_id:
        list_xslt:
        detail_xslt:
        template_xsl_rendering_id:

    Returns:
        TemplateXSLRendering - The updated/created object.
    """
    try:
        template_xsl_rendering = get_by_id(template_xsl_rendering_id)
        template_xsl_rendering.list_xslt = list_xslt
        template_xsl_rendering.detail_xslt = detail_xslt
    except Exception as exception:
        logger.warning("Exception when saving TemplateXSLRendering object: %s" % str(exception))
        template_xsl_rendering = TemplateXslRendering(template=template_id, list_xslt=list_xslt,
                                                      detail_xslt=detail_xslt)

    return _upsert(template_xsl_rendering)


def _upsert(template_xsl_rendering):
    """ Upsert an TemplateXslRendering.

    Args:
        template_xsl_rendering: TemplateXslRendering instance.

    Returns:
        TemplateXslRendering instance

    """
    return template_xsl_rendering.save()


def delete(template_xsl_rendering):
    """ Delete an TemplateXslRendering.

    Args:
        template_xsl_rendering: TemplateXslRendering to delete.

    """
    template_xsl_rendering.delete()


def get_by_id(template_xsl_rendering_id):
    """ Get an TemplateXslRendering document by its id.

    Args:
        template_xsl_rendering_id: Id.

    Returns:
        TemplateXslRendering object.

    Raises:
        DoesNotExist: The TemplateXslRendering doesn't exist.
        ModelError: Internal error during the process.

    """
    return TemplateXslRendering.get_by_id(template_xsl_rendering_id)


def get_by_template_id(template_id):
    """Get TemplateXslRendering by its template id.

    Args:
        template_id: Template id.

    Returns:
        The TemplateXslRendering instance.

    """
    return TemplateXslRendering.get_by_template_id(template_id)


def get_by_template_hash(template_hash):
    """Get TemplateXslRendering by its template hash.

    Args:
        template_hash: Template hash.

    Returns:
        The TemplateXslRendering instance.

    """
    instance = None
    # Get list of templates with the given hash
    templates = template_api.get_all_by_hash(template_hash)
    # Check if one of the templates has a xslt. Stop when found.
    # FIXME: Check if this process is okay (no solutions to distinguish templates from same hash)
    for template in templates:
        try:
            instance = TemplateXslRendering.get_by_template_id(template.id)
            break
        except exceptions.DoesNotExist as e:
            logger.warning("get_by_template_hash threw an exception: ".format(str(e)))

    if instance is None:
        raise exceptions.DoesNotExist("No TemplateXslRendering found with the given template hash")

    return instance


def get_all():
    """Get all TemplateXslRendering.

    Returns:
        List of TemplateXslRendering.

    """
    return TemplateXslRendering.get_all()
