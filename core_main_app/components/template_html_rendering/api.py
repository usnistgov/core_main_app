""" Template HTML rendering API
"""

from core_main_app.components.template_html_rendering.models import (
    TemplateHtmlRendering,
)
from django.template import Template as DjangoTemplate, Context


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


def upsert(template_html_rendering):
    """Save or Updates the template.

    Args:
        template_html_rendering:

    Returns:

    """
    template_html_rendering.save()
    return template_html_rendering


def get_by_id(template_html_rendering_id):
    """Get a template.

    Args:
        template_html_rendering_id:

    Returns:

    """
    return TemplateHtmlRendering.get_by_id(template_html_rendering_id)


def get_all():
    """List all TemplateHtmlRendering.

    Returns:

    """
    return TemplateHtmlRendering.get_all()


def delete(template_html_rendering):
    """Delete the template.

    Returns:

    """
    template_html_rendering.delete()


def render_data(template_html_rendering, data, rendering):
    """render_data.

    Args:
        template_html_rendering:
        data:
        rendering:

    Returns:

    """
    template_rendering = DjangoTemplate(
        getattr(template_html_rendering, rendering)
    )

    # Render the template with the context
    context = Context({"dict_content": data.get_dict_content()})
    return template_rendering.render(context)
