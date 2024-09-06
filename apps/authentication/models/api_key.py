"""

API Key Model

This model is used to store the API keys for the users.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from datetime import datetime
from typing import Optional

from pydantic import field_validator, model_validator

from apps.authentication.methods.api_key_util_methods import hash_api_key
from apps.common.models.base_model import BaseModel


class APIKey(BaseModel, table=True):
    """API Key model"""

    key: str
    short_key: Optional[str]
    title: str
    description: str
    expiry_date: Optional[datetime]

    @property
    def enabled(self):
        """
        Check if the API key is enabled to use.
        """
        if not self.expiry_date:
            return self.is_active
        return self.expiry_date > datetime.now() and self.is_active

    @field_validator("key", mode="before")
    @classmethod
    def validate_key(cls, value):
        """Validate key"""
        if not value:
            raise ValueError("Key is required")

        if not isinstance(value, str):
            raise ValueError("Key must be a string")

        return value

    @model_validator(mode="after")
    def hash_and_store_key(self):
        """Generate short key from the key"""
        self.key = hash_api_key(self.key)
        print(type(self.key), "keASDASDy")
        return self
