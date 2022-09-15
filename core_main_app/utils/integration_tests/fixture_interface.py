""" Fixture interface
"""


class FixtureInterface:
    """Represent the fixture interface with methods which must be implemented."""

    def insert_data(self):
        """Insert fixture's data

        Returns:

        """
        raise NotImplementedError()
