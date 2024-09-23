"""

API Key Util Methods

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import hashlib
import os
import secrets


def generate_api_key() -> str:
    """Generate an API key."""
    return secrets.token_urlsafe(32)


def hash_api_key(api_key: str) -> str:
    """Hash an API key."""
    salt = os.urandom(16)
    hashed_key = hashlib.pbkdf2_hmac("sha256", api_key.encode("utf-8"), salt, 100000)
    return f"{salt.hex()}:{hashed_key.hex()}"


def verify_api_key(stored_hashed_key: str, provided_api_key: str) -> bool:
    """Verify an API key."""
    salt_hex, stored_hash_hex = stored_hashed_key.split(":")
    salt = bytes.fromhex(salt_hex)
    hashed_provided_key = hashlib.pbkdf2_hmac(
        "sha256", provided_api_key.encode("utf-8"), salt, 100000
    )
    return stored_hash_hex == hashed_provided_key.hex()
