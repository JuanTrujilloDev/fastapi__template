"""
Password utility methods.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from apps.authentication.constants.hash_constants import STRING_HASHER


def hash_string(string: str) -> str:
    """
    Hash the string using the STRING_HASHER.

    Args:
        string (str): String to hash

    Returns:
        str: Hashed string ready for storage
    """
    return STRING_HASHER.hash(string)


def verify_strings(stored_string: str, string: str) -> bool:
    """
    Verify the string using the STRING_HASHER.

    Args:
        stored_string (str): Stored hashed value
        string (str): Plain text string to verify

    Returns:
        bool: True if the password is correct
    """
    return STRING_HASHER.verify(string, stored_string)
