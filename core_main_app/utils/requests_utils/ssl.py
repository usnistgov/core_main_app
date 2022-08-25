""" SSL utils
"""
import logging
from os import listdir
from os.path import isdir, exists

from core_main_app.commons.exceptions import SSLError

logger = logging.getLogger(__name__)


def check_ssl_certificates_dir_setting(ssl_certificates_dir):
    """Check that SSL_CERTIFICATES_DIR is correctly set. Log errors otherwise.

    Args:
        ssl_certificates_dir:

    Returns:

    """
    accepted_values_msg = (
        " Accepted values are either a boolean, in which case it controls whether requests verify"
        " the server's TLS certificate, or a string, in which case it must be a path"
        " to a CA bundle to use."
    )

    # if setting is a boolean
    if isinstance(ssl_certificates_dir, bool):
        if ssl_certificates_dir:
            logger.info(
                "SSL_CERTIFICATES_DIR: SSL certificate verification is enabled."
            )
        else:
            logger.warning(
                "SSL_CERTIFICATES_DIR: SSL certificate verification is disabled."
            )

    # if setting is a string
    elif isinstance(ssl_certificates_dir, str):
        # if the path does not exist
        if not exists(ssl_certificates_dir):
            logger.error(
                "SSL_CERTIFICATES_DIR is set but the file or directory does not exist. %s ",
                accepted_values_msg,
            )
            raise SSLError("SSL_CERTIFICATES_DIR improperly configured.")
        # if the path is a directory
        if isdir(ssl_certificates_dir):
            # if the directory is empty
            if not listdir(ssl_certificates_dir):
                logger.error(
                    "SSL_CERTIFICATES_DIR is set to an empty directory. %s",
                    accepted_values_msg,
                )
                raise SSLError("SSL_CERTIFICATES_DIR improperly configured.")

    # setting is not a boolean or a string
    else:
        logger.error("SSL_CERTIFICATES_DIR: Bad value. %s", accepted_values_msg)
        raise SSLError("SSL_CERTIFICATES_DIR improperly configured.")
