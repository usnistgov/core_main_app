""" Logger utils
"""


def set_generic_handler(logging_dict, name, level, filename, max_size, backup_count, class_name):
    """ Set a handler based on the parameters.

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
    logging_dict['handlers'].update({
        name: {
            'level': level,
            'class': class_name,
            'filename': filename,
            'maxBytes': max_size,
            'backupCount': backup_count,
            'formatter': 'fmt-default',
        },
    })


def set_generic_logger(logging_dict, name, level, list_handler):
    """ Set a logger based on the parameters.

    Args
        logging_dict:
        name:
        level:
        list_handler:

    Returns:
    """
    logging_dict['loggers'].update({
        name: {
            'handlers': list_handler,
            'level': level,
            'propagate': False,
        },
    })
