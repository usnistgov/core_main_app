""" View builder for view data page.
"""
import logging

from django.conf import settings as conf_settings

from core_main_app.commons import exceptions
from core_main_app.components.template_xsl_rendering import (
    api as template_xsl_rendering_api,
)

logger = logging.getLogger(__name__)


def build_page(
    data_object, display_admin_version=False, display_download_options=False
):
    """Generic page building data

    Args:
        data_object:
        display_admin_version:
        display_download_options:

    Returns:
    """
    page_info = {
        "error": None,
        "context": {},
        "assets": {},
        "modals": [],
    }

    try:
        (
            display_xslt_selector,
            template_xsl_rendering,
            xsl_transformation_id,
        ) = xslt_selector(
            _get_field(_get_field(data_object, "template"), "id")
        )

        page_info["context"] = {
            "data": data_object,
            "share_pid_button": False,
            "template_xsl_rendering": template_xsl_rendering,
            "xsl_transformation_id": xsl_transformation_id,
            "can_display_selector": display_xslt_selector,
            "display_download_options": display_download_options,
            "page_title": _get_field(data_object, "title"),
        }

        page_info["assets"] = {
            "js": [
                {
                    "path": "core_main_app/common/js/XMLTree.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/user/js/data/detail.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/user/js/data/change_display.js",
                    "is_raw": False,
                },
            ],
            "css": [
                "core_main_app/common/css/XMLTree.css",
                "core_main_app/common/css/detail.css",
            ],
        }

        if display_download_options:
            page_info["assets"]["js"].extend(
                [
                    {
                        "path": "core_main_app/common/js/data_detail.js",
                        "is_raw": False,
                    },
                    {
                        "path": "core_main_app/common/js/modals/download.js",
                        "is_raw": False,
                    },
                ]
            )
            page_info["assets"]["css"].append(
                "core_main_app/common/css/modals/download.css"
            )
            page_info["modals"].append(
                "core_main_app/common/modals/download-options.html"
            )

        if "core_file_preview_app" in conf_settings.INSTALLED_APPS:
            page_info["assets"]["js"].extend(
                [
                    {
                        "path": "core_file_preview_app/user/js/file_preview.js",
                        "is_raw": False,
                    }
                ]
            )
            page_info["assets"]["css"].append(
                "core_file_preview_app/user/css/file_preview.css"
            )
            page_info["modals"].append(
                "core_file_preview_app/user/file_preview_modal.html"
            )

        if "core_linked_records_app" in conf_settings.INSTALLED_APPS:
            from core_linked_records_app.system.pid_settings import (
                api as pid_settings_system_api,
            )

            if pid_settings_system_api.get().auto_set_pid:
                page_info["context"]["share_pid_button"] = True
                page_info["assets"]["js"].extend(
                    [
                        {
                            "path": "core_main_app/user/js/sharing_modal.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_linked_records_app/user/js/sharing/data_detail.js",
                            "is_raw": False,
                        },
                    ]
                )
                page_info["assets"]["css"].append(
                    "core_main_app/common/css/share_link.css"
                )
                page_info["modals"].append(
                    "core_linked_records_app/user/sharing/data_detail/modal.html"
                )
    except exceptions.DoesNotExist:
        page_info["error"] = "Data not found"
    except exceptions.ModelError:
        page_info["error"] = "Model error"
    except Exception as exception:
        page_info["error"] = str(exception)
    finally:
        return page_info


def _get_field(data_object, field):
    """Get value of field from object or dict

    Args:
        data_object:
        field:

    Returns:

    """
    if field not in ["title", "template", "id"]:
        return None
    # If data is None, title is None
    if not data_object:
        return None
    # If data is a Data, return data.field
    if hasattr(data_object, field):
        return getattr(data_object, field)
    # If data is a dict, return data['field']
    if isinstance(data_object, dict):
        return data_object.get(field, None)
    return None


def xslt_selector(template_id):
    """Setup Xslt Selector

    Args:
        template_id

    Return:

    """

    display_xslt_selector = True
    try:
        template_xsl_rendering = template_xsl_rendering_api.get_by_template_id(
            template_id
        )
        xsl_transformation_id = (
            template_xsl_rendering.default_detail_xslt.id
            if template_xsl_rendering.default_detail_xslt
            else None
        )
        if template_xsl_rendering.list_detail_xslt.count() == 0 or (
            template_xsl_rendering.default_detail_xslt is not None
            and template_xsl_rendering.list_detail_xslt.count() == 1
        ):
            display_xslt_selector = False

    except Exception as exception:
        logger.warning(
            "An exception occurred when retrieving XSLT: %s",
            str(exception),
        )
        display_xslt_selector = False
        template_xsl_rendering = None
        xsl_transformation_id = None

    return display_xslt_selector, template_xsl_rendering, xsl_transformation_id


def render_page(request, render_function, template, context):
    """render page

    Args:
        request:
        render_function:
        template:
        context:

    Returns:

    """
    if context["error"] is not None:
        return render_function(
            request,
            "core_main_app/common/commons/error.html",
            context={"error": context["error"]},
        )

    return render_function(
        request,
        template,
        context=context["context"],
        assets=context["assets"],
        modals=context["modals"],
    )
