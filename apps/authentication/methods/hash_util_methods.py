"""
Password utility methods.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from apps.authentication.constants.hash_constants import STRING_HASHER


def hash_string_with_secret_key(string: str) -> str:
    """
    First encrypt the password with Fernet, then hash with bcrypt.

    Args:
        string (str): String to encrypt and hash.

    Returns:
        str: Hashed string ready for storage
    """
    # TODO: Implement encryption logic
    return STRING_HASHER.hash(string)


def verify_strings(stored_string: str, string: str) -> bool:
    """
    Verify the password using the same encrypt-then-hash approach.

    Args:
        stored_string (str): Stored hashed value
        string (str): Plain text string to verify

    Returns:
        bool: True if the password is correct
    """
    return STRING_HASHER.verify(stored_string, string)
