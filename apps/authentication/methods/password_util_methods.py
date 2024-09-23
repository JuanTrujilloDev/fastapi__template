"""

Password utility methods.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import hashlib
import hmac

import bcrypt

from fastapi__template.settings import SETTINGS


def hash_password_with_secret_key(password: str) -> str:
    """Hash the password with the secret key."""
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    # Generate HMAC of the hashed password using the secret key
    hmac_hash = hmac.new(
        SETTINGS.SECRET_KEY.encode("utf-8"), hashed_password, hashlib.sha512
    ).hexdigest()

    # Store salt and HMAC together
    return f"{salt.decode('utf-8')}:{hmac_hash}"


def verify_password(stored_data: str, password: str) -> bool:
    """Verify the password."""
    salt, stored_hmac = stored_data.split(":")
    # Hash the password using the same salt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt.encode("utf-8"))

    # Generate HMAC for the hashed password
    hmac_hash = hmac.new(
        SETTINGS.SECRET_KEY.encode("utf-8"), hashed_password, hashlib.sha512
    ).hexdigest()

    return hmac.compare_digest(hmac_hash, stored_hmac)
