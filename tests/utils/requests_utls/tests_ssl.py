""" SSL utils test class
"""
from unittest import TestCase

from core_main_app.commons.exceptions import SSLError
from core_main_app.utils.requests_utils.ssl import check_ssl_certificates_dir_setting


class TestCheckSslCertificatesDirSetting(TestCase):
    """TestCheckSslCertificatesDirSetting"""

    def test_check_ssl_certificates_dir_setting_ok_when_set_to_true(self):
        """test check ssl certificates dir setting ok when set to True

        Returns:

        """
        check_ssl_certificates_dir_setting(True)

    def test_check_ssl_certificates_dir_setting_ok_when_set_to_false(self):
        """test check ssl certificates dir setting ok when set to False

        Returns:

        """
        check_ssl_certificates_dir_setting(False)

    def test_check_ssl_certificates_dir_setting_raises_error_if_bad_parameter_type(
        self,
    ):
        """test check ssl certificates dir setting raises error if bad parameter type

        Returns:

        """
        with self.assertRaises(SSLError):
            check_ssl_certificates_dir_setting(1)

    def test_check_ssl_certificates_dir_setting_fails_when_set_to_bad_location(self):
        """test check ssl certificates dir setting fails when set to bad location

        Returns:

        """
        fake_dir_path = "./fake/dir"
        with self.assertRaises(SSLError):
            check_ssl_certificates_dir_setting(fake_dir_path)
