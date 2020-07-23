""" View builder for view data page.
"""
from core_main_app.components.data import api as data_api
from core_main_app.settings import INSTALLED_APPS
from core_main_app.commons import exceptions


def build_page(data_id, user, display_admin_version=False):
    """ Generic page building data

    Args:
        data_id:
        user:
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
        page_info["context"] = {
            "data": data_api.get_by_id(data_id, user),
            "share_pid_button": False,
        }

        page_info["assets"] = {
            "js": [
                {"path": "core_main_app/common/js/XMLTree.js", "is_raw": False},
                {"path": "core_main_app/user/js/data/detail.js", "is_raw": False},
            ],
            "css": ["core_main_app/common/css/XMLTree.css"],
        }

        if "core_file_preview_app" in INSTALLED_APPS:
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

        if "core_linked_records_app" in INSTALLED_APPS and not display_admin_version:
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
