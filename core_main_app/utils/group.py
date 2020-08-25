"""
    Utils for groups
"""


def remove_list_object_from_list(list_object, list_object_to_be_removed):
    """Remove list of objects from another list of objects.

    Args:
            list_object:
            list_object_to_be_removed:
    Returns:
    """

    for group in list_object_to_be_removed:
        if group in list_object:
            list_object.remove(group)
