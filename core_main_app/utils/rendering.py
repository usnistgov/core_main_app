from django.shortcuts import render as django_render


def render(request, template_name, modals=None, assets=None, context=None):
    """Renders a selected template with the project's theme

    Parameters:
        request:
        template_name:
        modals:
        assets:
        context:

    Returns:
        HTTPResponse
    """
    modals = modals if modals is not None else []
    assets = assets if assets is not None else {"css": [], "js": []}
    context = context if context is not None else {}

    # Rebuild the context for the app_wrapper template
    context = {
        "template": template_name,
        "modals": modals,
        "assets": assets,
        "data": context
    }

    return django_render(request, "core_main_app/app_wrapper.html", context)
