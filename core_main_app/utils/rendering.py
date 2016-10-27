from django.shortcuts import render as django_render


def render(request, template_name, context):
    """ Renders a selected template with the project's theme

    Parameters:
        request:
        template_name:
        context:

    Returns:
        HTTPResponse
    """
    context["template"] = template_name

    return django_render(request, "core_main_app/app_wrapper.html", context)
