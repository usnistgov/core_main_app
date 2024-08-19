""" Template HTML rendering API
"""

from core_main_app.components.template_html_rendering.models import (
    TemplateHtmlRendering,
)


def get_by_template_id(template_id):
    """Get TemplateHtmlRendering by its template id.

    Args:
        template_id: Template id.

    Returns:
        The TemplateHtmlRendering instance.

    """
    return TemplateHtmlRendering.get_by_template_id(template_id)


def get_by_template_hash(template_hash):
    """Get TemplateHtmlRendering by its template hash.

    Args:
        template_hash: Template hash.

    Returns:
        The TemplateHtmlRendering instance.

    """
    return TemplateHtmlRendering.get_by_template_hash(template_hash)
