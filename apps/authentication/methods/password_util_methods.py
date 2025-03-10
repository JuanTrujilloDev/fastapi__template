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


def hash_password_with_secret_key(password: str) -> Tuple[str, bytes]:
    """
    Hash the password with the secret key.

    Args:
        password (bytes): Password.

    Returns:
        Tuple[bytes, bytes]: Hashed password and salt.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    hashed_password_with_secret_key = hmac.new(
        settings.SECRET_KEY.encode("utf-8"), hashed_password, hashlib.sha512
    ).digest()
    return hashed_password_with_secret_key, salt


def verify_password(stored_password: bytes, stored_salt: bytes, password: str) -> bool:
    """
    Verify the password.

    Gets the stored data and password and verifies if the password is correct.

    Args:
        stored_data (bytes): Stored data.
        password (bytes): Password.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), stored_salt)
    hashed_password_with_secret_key = hmac.new(
        settings.SECRET_KEY.encode("utf-8"), hashed_password, hashlib.sha512
    ).digest()
    return hmac.compare_digest(hashed_password_with_secret_key, stored_password)
