""" Logger utils
"""
import copy


def update_logger_with_local_app(logging_dict, local_logger_conf, list_app):
    """Update the logger with local app.

    Args:
        logging_dict:
        local_logger_conf:
        list_app:
    Returns:
    """
    logging_dict["loggers"].update(
        {app: copy.deepcopy(local_logger_conf) for app in get_list_local_app(list_app)}
    )


def get_list_local_app(list_app):
    """Get the list of local apps.

    Args:
         list_app:
    Return:
    """
    local_apps = []
    for app in list_app:
        if app.startswith("core") and "." not in app:
            local_apps.append(app)
    return local_apps


def set_generic_handler(
    logging_dict, name, level, filename, max_size, backup_count, class_name
):
    """Set a handler based on the parameters.

    Args
        logging_dict:
        name:
        level:
        filename:
        max_size:
        backup_count:
        class_name:

    Returns:
    """
    logging_dict["handlers"].update(
        {
            name: {
                "level": level,
                "class": class_name,
                "filename": filename,
                "maxBytes": max_size,
                "backupCount": backup_count,
                "formatter": "fmt-default",
            },
        }
    )


def set_generic_logger(logging_dict, name, level, list_handler):
    """Set a logger based on the parameters.

    Args
        logging_dict:
        name:
        level:
        list_handler:

    Returns:
    """
    logging_dict["loggers"].update(
        {
            name: {
                "handlers": list_handler,
                "level": level,
                "propagate": False,
            },
        }
    )
