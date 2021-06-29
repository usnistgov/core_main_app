""" View builder for view data page.
"""
import logging

from core_main_app import settings
from core_main_app.commons import exceptions
from core_main_app.components.template_xsl_rendering import (
    api as template_xsl_rendering_api,
)
from bson import ObjectId


logger = logging.getLogger(__name__)


def build_page(data_object, display_admin_version=False):
    """Generic page building data

    Args:
        data_object:
        display_admin_version:

    Returns:
    """
    page_info = {
        "error": None,
        "context": dict(),
        "assets": dict(),
        "modals": list(),
    }

    try:
        display_xslt_selector = True
        try:
            template_xsl_rendering = template_xsl_rendering_api.get_by_template_id(
                data_object.template.id
            )
            xsl_transformation_id = (
                template_xsl_rendering.default_detail_xslt.id
                if template_xsl_rendering.default_detail_xslt
                else None
            )
            if not template_xsl_rendering.list_detail_xslt or (
                template_xsl_rendering.default_detail_xslt is not None
                and len(template_xsl_rendering.list_detail_xslt) == 1
            ):
                display_xslt_selector = False

            if xsl_transformation_id is not None:
                xsl_transformation_id = ObjectId(xsl_transformation_id)
        except Exception as exception:
            logger.warning(
                "An exception occured when retrieving XSLT: %s" % str(exception)
            )
            display_xslt_selector = False
            template_xsl_rendering = None
            xsl_transformation_id = None

        page_info["context"] = {
            "data": data_object,
            "share_pid_button": False,
            "template_xsl_rendering": template_xsl_rendering,
            "xsl_transformation_id": xsl_transformation_id,
            "can_display_selector": display_xslt_selector,
        }

        page_info["assets"] = {
            "js": [
                {"path": "core_main_app/common/js/XMLTree.js", "is_raw": False},
                {"path": "core_main_app/user/js/data/detail.js", "is_raw": False},
                {
                    "path": "core_main_app/user/js/data/change_display.js",
                    "is_raw": False,
                },
            ],
            "css": ["core_main_app/common/css/XMLTree.css"],
        }

        if "core_file_preview_app" in settings.INSTALLED_APPS:
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

        if (
            "core_linked_records_app" in settings.INSTALLED_APPS
            and not display_admin_version
        ):
            from core_linked_records_app.components.pid_settings import (
                api as pid_settings_api,
            )

            if pid_settings_api.get().auto_set_pid:
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
                page_info["modals"].append(
                    "core_linked_records_app/user/sharing/data_detail/modal.html"
                )
    except exceptions.DoesNotExist:
        page_info["error"] = "Data not found"
    except exceptions.ModelError:
        page_info["error"] = "Model error"
    except Exception as e:
        page_info["error"] = str(e)
    finally:
        return page_info


def render_page(request, render_function, template, context):
    if context["error"] is None:
        return render_function(
            request,
            template,
            context=context["context"],
            assets=context["assets"],
            modals=context["modals"],
        )
    else:
        return render_function(
            request,
            "core_main_app/common/commons/error.html",
            context={"error": context["error"]},
        )
