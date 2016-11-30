""" Fixture interface
"""


class FixtureInterface(object):
    """ Represents the fixture interface with methods which must be implemented
    """

    def insert_data(self):
        """ Insert fixture's data

        Returns:

        """
        raise NotImplementedError()
