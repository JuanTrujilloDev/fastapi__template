"""

API Key Model

This model is used to store the API keys for the users.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import secrets
from datetime import datetime
from typing import ClassVar, Optional

from pydantic import model_validator

from apps.authentication.methods.api_key_util_methods import hash_api_key
from apps.common.models.base_model import BaseModel


class APIKey(BaseModel, table=True):
    """API Key model"""

    HASH_METHOD: ClassVar = "sha256"

    key: Optional[bytes]
    short_key: Optional[str]
    title: str
    description: str
    expiry_date: Optional[datetime]

    class Config:
        """Pydantic config"""

        orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True

    @property
    def enabled(self):
        """
        Check if the API key is enabled to use.
        """
        return self.expiry_date > datetime.now() and self.is_active

    @model_validator(mode="before")
    def generate_key(self):
        """Generate key to be used as API key"""
        random_key = secrets.token_urlsafe(32)
        self.key = hash_api_key(random_key)
        self.short_key = random_key[:5]
        return self
