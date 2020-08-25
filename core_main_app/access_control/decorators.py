"""Access control decorator
"""


def access_control(check_func):
    """Access control decorator.

    Args:
        check_func: function that checks access

    Returns:

    """

    def _access_control(func):
        """Decorator.

        Args:
            func: function on which the decorator is attached.

        Returns:

        """

        def wrapper(*args, **kwargs):
            """Function wrapper.

            Args:
                *args:
                **kwargs:

            Returns:

            """
            return check_func(func, *args, **kwargs)

        return wrapper

    return _access_control
