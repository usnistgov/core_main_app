""" TemplateXslRendering API calls
"""
import logging

from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import ApiError
from core_main_app.components.template import api as template_api
from core_main_app.components.template_xsl_rendering.models import TemplateXslRendering

logger = logging.getLogger(__name__)


def add_or_delete(
    template_id,
    list_xslt,
    default_detail_xslt,
    list_detail_xslt,
    template_xsl_rendering_id=None,
):
    """Manage the saving of a TemplateXslRendering. If no XSLTs have been given,
    deletes the instance.

    Args:

        template_id: TemplateXslRendering.
        list_xslt: XSLT.
        default_detail_xslt: XSLT.
        list_detail_xslt:
        template_xsl_rendering_id: Instance id.

    Returns:

    """
    # Boolean to know if we need this instance in database, i.e there are XSLTs information.
    need_to_be_kept = (
        list_xslt is not None
        or default_detail_xslt is not None
        or list_detail_xslt is not None
    )

    if need_to_be_kept:
        return upsert(
            template_id,
            list_xslt,
            default_detail_xslt,
            list_detail_xslt,
            template_xsl_rendering_id,
        )
    else:
        try:
            if template_xsl_rendering_id:
                template_xsl_rendering = get_by_id(template_xsl_rendering_id)
                delete(template_xsl_rendering)

            return None
        except Exception:
            raise ApiError("An error occured while deleting the TemplateXSLRendering")


def set_list_detail_xslt(template_xsl_rendering, list_detail_xslt):
    """Set list of detail_xslt to a TemplateXslRendering

    Args:
        template_xsl_rendering
        list_detail_xslt

    Returns:

    """
    template_xsl_rendering.list_detail_xslt = list_detail_xslt
    _set_default_detail(template_xsl_rendering)
    template_xsl_rendering.save()


def add_detail_xslt(template_xsl_rendering, detail_xslt):
    """Add new detail xslt to a TemplateXslRendering

    Args:
        template_xsl_rendering
        detail_xslt

    Returns:

    """
    # Check if xslt exists in the list
    if detail_xslt not in template_xsl_rendering.list_detail_xslt:

        # Set the new xslt as default detail if the list is empty
        if not template_xsl_rendering.list_detail_xslt:
            template_xsl_rendering.default_detail_xslt = detail_xslt
        template_xsl_rendering.list_detail_xslt.append(detail_xslt)
        template_xsl_rendering.save()
    else:
        raise Exception("The xslt already exists in the list")


def delete_detail_xslt(template_xsl_rendering, detail_xslt):
    """Remove a detail_xslt from the details list. If this is a default detail xslt,
    set another default xslt.

    Args:
        template_xsl_rendering
        detail_xslt

    Returns:

    """

    if detail_xslt in template_xsl_rendering.list_detail_xslt:
        template_xsl_rendering.list_detail_xslt.remove(detail_xslt)

        # Check that removed detail xslt is not defined by default
        if detail_xslt == template_xsl_rendering.default_detail_xslt:
            _set_default_detail(template_xsl_rendering)

        template_xsl_rendering.save()
    else:
        raise Exception("The xslt does not exist in the list")


def set_default_detail_xslt(template_xsl_rendering, detail_xslt):
    """Set default detail_xslt

    Args:
        template_xsl_rendering
        detail_xslt

    Returns:

    """
    # Check if xslt exists in the list
    if detail_xslt in template_xsl_rendering.list_detail_xslt:
        template_xsl_rendering.default_detail_xslt = detail_xslt
        template_xsl_rendering.save()
    else:
        raise Exception("The xslt does not exist in the list")


def upsert(
    template_id,
    list_xslt,
    default_detail_xslt,
    list_detail_xslt,
    template_xsl_rendering_id=None,
):
    """Update or create a XSL Template rendering object

    Args:
        template_id:
        list_xslt:
        default_detail_xslt:
        list_detail_xslt:
        template_xsl_rendering_id:

    Returns:
        TemplateXSLRendering - The updated/created object.
    """
    try:
        template_xsl_rendering = get_by_id(template_xsl_rendering_id)
        template_xsl_rendering.list_xslt = list_xslt
        template_xsl_rendering.default_detail_xslt = default_detail_xslt
        template_xsl_rendering.list_detail_xslt = list_detail_xslt
    except Exception as exception:
        logger.warning(
            "Exception when saving TemplateXSLRendering object: %s" % str(exception)
        )
        template_xsl_rendering = TemplateXslRendering(
            template=template_id,
            list_xslt=list_xslt,
            default_detail_xslt=default_detail_xslt,
            list_detail_xslt=list_detail_xslt,
        )

    return _upsert(template_xsl_rendering)


def _upsert(template_xsl_rendering):
    """Upsert an TemplateXslRendering.

    Args:
        template_xsl_rendering: TemplateXslRendering instance.

    Returns:
        TemplateXslRendering instance

    """
    return template_xsl_rendering.save()


def delete(template_xsl_rendering):
    """Delete an TemplateXslRendering.

    Args:
        template_xsl_rendering: TemplateXslRendering to delete.

    """
    template_xsl_rendering.delete()


def get_by_id(template_xsl_rendering_id):
    """Get an TemplateXslRendering document by its id.

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
    # FIXME: Check if this process is okay (no solutions to distinguish templates from same hash)
    return TemplateXslRendering.get_by_template_hash(template_hash)


def get_all():
    """Get all TemplateXslRendering.

    Returns:
        List of TemplateXslRendering.

    """
    return TemplateXslRendering.get_all()


def _set_default_detail(template_xsl_rendering):

    if template_xsl_rendering.list_detail_xslt:
        template_xsl_rendering.default_detail_xslt = (
            template_xsl_rendering.list_detail_xslt[0]
        )
    else:
        template_xsl_rendering.default_detail_xslt = None
