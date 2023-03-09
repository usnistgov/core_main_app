""" Parser utils test class
"""
from unittest import TestCase

from core_main_app.utils.parser import get_parser
from core_parser_app.tools.parser.parser import XSDParser


class TestGetParser(TestCase):
    """Test to_bool"""

    def test_get_parser_returns_parser(self):
        """test_get_parser_returns_parser

        Returns:

        """
        self.assertIsInstance(get_parser(), XSDParser)
