"""
Password utility methods.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import bcrypt


def hash_string(string: str) -> str:
    """
    Hash the string using the STRING_HASHER.

    Args:
        string (str): String to hash

    Returns:
        str: Hashed string ready for storage
    """
    string_bytes = string.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_string = bcrypt.hashpw(password=string_bytes, salt=salt)
    return hashed_string.decode("utf-8")


def verify_strings(stored_string: str, string: str) -> bool:
    """
    Verify the string using the STRING_HASHER.

    Args:
        stored_string (str): Stored hashed value
        string (str): Plain text string to verify

    Returns:
        bool: True if the password is correct
    """
    string_bytes = string.encode("utf-8")
    return bcrypt.checkpw(
        password=string_bytes, hashed_password=stored_string.encode("utf-8")
    )
