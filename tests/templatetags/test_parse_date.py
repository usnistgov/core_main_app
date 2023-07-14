""" Unit tests of parse_date templatetag
"""
from unittest.case import TestCase
from unittest.mock import patch

from core_main_app.templatetags.parse_date import parse_date
from core_main_app.utils.datetime import datetime_now


class TestParseDate(TestCase):
    """Test parse_date"""

    def test_parse_date_with_datetime_returns_same_value(self):
        """test_parse_date_with_datetime_returns_same_value

        Returns:

        """
        date = datetime_now()
        self.assertEqual(date, parse_date(date))

    def test_parse_date_with_datetime_string_returns_datetime(self):
        """test_parse_date_with_datetime_string_returns_datetime

        Returns:

        """
        date = datetime_now()
        date_str = str(date)
        self.assertEqual(date, parse_date(date_str))

    def test_parse_date_with_invalid_datetime_string_returns_none(self):
        """test_parse_date_with_invalid_datetime_string_returns_none

        Returns:

        """
        date = datetime_now()
        date_str = str(date) + "bad"
        self.assertIsNone(parse_date(date_str))

    @patch("django.utils.dateparse.parse_datetime")
    def test_parse_date_with_value_error_returns_none(
        self, mock_parsedatetime
    ):
        """test_parse_date_with_value_error_returns_none

        Returns:

        """
        date = datetime_now()
        date_str = str(date)
        mock_parsedatetime.side_effect = ValueError()
        self.assertIsNone(parse_date(date_str))
