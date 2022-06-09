""" Checksum test class
"""
from os.path import join, dirname, abspath
from unittest import TestCase

from core_main_app.commons.exceptions import CoreError
from core_main_app.utils.checksum import compute_checksum

RESOURCES_PATH = join(dirname(abspath(__file__)), "data")


class TestComputeChecksum(TestCase):
    def test_compute_checksum_when_algo_found(self):
        bytes_obj = b"this is a test."
        checksum = compute_checksum(bytes_obj, "MD5")
        self.assertIsNotNone(checksum)

    def test_compute_raises_error_if_algo_not_found(self):
        bytes_obj = b"this is a test."
        with self.assertRaises(CoreError):
            compute_checksum(bytes_obj, "TEST")

    def test_compute_file_md5_returns_expected_hash(self):
        with open(join(RESOURCES_PATH, "expand.png"), "rb") as file:
            checksum = compute_checksum(file, "MD5")
            # MD5 (expand.png) = f767652a18f716db2f0f4f5cd74b5067
            self.assertEqual(checksum, "f767652a18f716db2f0f4f5cd74b5067")
