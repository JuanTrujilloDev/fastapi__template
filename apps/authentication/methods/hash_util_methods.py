"""

Password utility methods.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import hashlib
import hmac
from typing import Tuple

import bcrypt

from fastapi__template.settings import settings


def hash_string_with_secret_key(string: str, salt: bytes) -> Tuple[str, bytes]:
    """
    Hash the password with the secret key.

    Args:
        string (str): String to hash.

    Returns:
        Tuple[bytes, bytes]: Hashed string with used salt.

    """
    hashed_string = bcrypt.hashpw(string.encode("utf-8"), salt)
    hashed_string_with_secret_key = hmac.new(
        settings.SECRET_KEY.encode("utf-8"), hashed_string, hashlib.sha512
    ).digest()
    return hashed_string_with_secret_key


def verify_strings(stored_string: bytes, stored_salt: bytes, string: str) -> bool:
    """
    Verify the password.

    Verify string compared to a hashed string with salt and secret key.

    Args:
        stored_string (bytes): Stored data
        stored_salt (bytes): Salt used to hash the string.
        string (bytes): String to compare.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    hashed_string = bcrypt.hashpw(string.encode("utf-8"), stored_salt)
    hashed_string_with_secret_key = hmac.new(
        settings.SECRET_KEY.encode("utf-8"), hashed_string, hashlib.sha512
    ).digest()
    return hmac.compare_digest(hashed_string_with_secret_key, stored_string)
