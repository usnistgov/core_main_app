""" Checksum utils
"""

import hashlib

from core_main_app.commons.exceptions import CoreError

CHECKSUM_ALGORITHMS = {
    "MD5": hashlib.md5,
    "SHA1": hashlib.sha1,
    "SHA256": hashlib.sha256,
    "SHA512": hashlib.sha512,
}


def compute_checksum(file, checksum_algorithm, block_size=4096):
    """Compute checksum for a file content (bytes)

    Args:
        file:
        checksum_algorithm:
        block_size:

    Returns:

    """
    # Check if selected algorithm is in the list
    if checksum_algorithm not in CHECKSUM_ALGORITHMS.keys():
        raise CoreError(
            f"CHECKSUM_ALGORITHM needs to be in: {CHECKSUM_ALGORITHMS.keys()}"
        )

    # Init hasher with selected algorithm
    hasher = CHECKSUM_ALGORITHMS[checksum_algorithm]()

    # If param is bytes
    if isinstance(file, bytes):
        # Update hasher
        hasher.update(file)
        # Return hash
        return hasher.hexdigest()

    # If file, read file, chunk by chunk
    for chunk in iter(lambda: file.read(block_size), b""):
        # Hash each chuck
        hasher.update(chunk)
    # Return hash
    return hasher.hexdigest()
