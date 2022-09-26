""" Rendering utils
"""
from os.path import splitext

from django.contrib.staticfiles import finders
from django.shortcuts import render as django_render


def _build_js_assets(js_assets):
    """Build js assets structure

    Args:
        js_assets:

    Returns:

    """
    updated_js_assets = []
    included_js_paths = [asset["path"] for asset in js_assets]

    for asset in js_assets:
        # By default an asset is not raw javascript
        if "is_raw" not in asset:
            asset["is_raw"] = False

        # By default asset are stored in the static dir
        if "is_external" not in asset:
            asset["is_external"] = False

        if not asset[
            "is_raw"
        ]:  # If an asset is not raw js, we look for raw js child file
            js_asset_splitext = splitext(asset["path"])
            js_raw_file = js_asset_splitext[0] + ".raw" + js_asset_splitext[1]

            # Test that the file exists and is not already included
            if (
                finders.find(js_raw_file) is not None
                and js_raw_file not in included_js_paths
            ):
                updated_js_assets.append({"path": js_raw_file, "is_raw": True})

        updated_js_assets.append(asset)

    return updated_js_assets


def _render(
    request,
    template_name,
    wrapper_name,
    modals=None,
    assets=None,
    context=None,
    use_theme=True,
):
    """Render a selected template.

    Args:
        request:
        template_name:
        wrapper_name:
        modals:
        assets:
        context:
        use_theme:

    Returns:

    """
    modals = modals if modals is not None else []
    assets = assets if assets is not None else {"css": [], "js": []}
    js_asset = assets["js"] if "js" in assets else []
    assets["js"] = _build_js_assets(js_asset)
    context = context if context is not None else {}

    # Rebuild the context for the app_wrapper template
    context = {
        "template": template_name,
        "modals": modals,
        "assets": assets,
        "data": context,
        "use_theme": use_theme,
    }

    return django_render(request, wrapper_name, context)


def render(
    request,
    template_name,
    modals=None,
    assets=None,
    context=None,
    use_theme=True,
):
    """Render a selected template with the project's theme or a default one.

    Parameters:
        request:
        template_name:
        modals:
        assets:
        context:
        use_theme:

    Returns:
        HTTPResponse
    """
    return _render(
        request,
        template_name,
        "core_main_app/_render/user/app_wrapper.html",
        modals,
        assets,
        context,
        use_theme,
    )


def admin_render(
    request, template_name, modals=None, assets=None, context=None
):
    """Render a selected template with the project's theme,

    Parameters:
        request:
        template_name:
        modals:
        assets:
        context:

    Returns:
        HTTPResponse
    """
    return _render(
        request,
        template_name,
        "core_main_app/_render/admin/app_wrapper.html",
        modals,
        assets,
        context,
    )
