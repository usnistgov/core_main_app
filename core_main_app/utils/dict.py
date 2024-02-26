""" Utilities for dictionaries
"""


def get_dict_keys(dictionary):
    """Retrieve all keys in a nested dictionary.

    Args:
        dictionary (dict): The dictionary to retrieve the keys from.

    Returns:
        set: The keys located in the dictionary.
    """
    keys = set()

    for key, value in dictionary.items():
        keys.add(key)
        if isinstance(value, dict):
            keys.update(get_dict_keys(value))

    return keys
