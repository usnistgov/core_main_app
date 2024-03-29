"""
    Iso8601 operation test class
"""

import datetime
from unittest import TestCase

from core_main_app.utils import datetime as datetime_utils


class TestDatetimeToUTCDatetimeIso8601(TestCase):
    """Test Date time To UTC Date time Iso 8601"""

    def test_valid_conversion(self):
        """test_valid_conversion"""
        # Arrange
        date_to_convert = datetime.datetime(2016, 11, 18, 8, 30)

        # Act
        result = datetime_utils.datetime_to_utc_datetime_iso8601(
            date_to_convert
        )

        # Assert
        self.assertEqual(result, "2016-11-18T08:30:00Z")


class TestUTCDatetimeIso8601ToDatetime(TestCase):
    """Test UTC Date time Iso 8601 To Datetime"""

    def test_valid_conversion(self):
        """test_valid_conversion"""
        # Arrange
        date_to_convert = "2016-11-18T08:30:00Z"

        # Act
        result = datetime_utils.utc_datetime_iso8601_to_datetime(
            date_to_convert
        )

        # Assert
        self.assertEqual(
            result,
            datetime.datetime(2016, 11, 18, 8, 30).replace(
                tzinfo=datetime.timezone.utc
            ),
        )

    def test_invalid_conversion(self):
        """test_invalid_conversion"""
        # Arrange
        date_to_convert = "20166-11-18T08:30:00Z"

        # Act # Assert
        with self.assertRaises(Exception):
            datetime_utils.utc_datetime_iso8601_to_datetime(date_to_convert)
