""" Enumeration
"""


def enum(**enums):
    """ Create an enumeration based on the args.

    Args:
        enums

    Returns:
    """
    return type('Enum', (), enums)
