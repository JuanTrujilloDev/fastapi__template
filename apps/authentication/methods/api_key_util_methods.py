"""

API Key Util Methods

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import base64
import hashlib
import hmac

from fastapi__template.settings import SETTINGS


def hash_api_key(api_key: str) -> str:
    """Hash API key."""
    base64_encoded_key = base64.b64encode(api_key)
    hashed_key = hmac.new(SETTINGS.secret_key, base64_encoded_key, hashlib.sha256)
    return hashed_key.hexdigest()
