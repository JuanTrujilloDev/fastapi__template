"""

API Key Model

This model is used to store the API keys for the users.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from datetime import date, datetime
from typing import Optional

from pydantic import field_validator, model_validator
from sqlmodel import Field

from apps.authentication.methods.api_key_util_methods import hash_api_key
from apps.common.models.base_model import BaseModel


class APIKey(BaseModel, table=True):
    """API Key model"""

    # TODO: Validate title and description
    key: str = Field(..., description="API Key")
    short_key: Optional[str] = Field(None, description="Short key")
    title: str = Field(..., description="Title")
    description: str = Field(None, description="Description")
    expiry_date: Optional[datetime] = Field(None, description="Expiry date")

    @property
    def enabled(self):
        """
        Check if the API key is enabled to use.
        """
        if not self.expiry_date:
            return self.is_active
        return self.expiry_date > datetime.now() and self.is_active

    @field_validator("expiry_date", mode="after")
    @classmethod
    def validate_expiry_date(cls, value: date):
        """Validate expiry date"""
        if value and value.date() < datetime.now().date():
            raise ValueError("Expiry date should be greater than today.")

        return value

    @model_validator(mode="after")
    def generate_hash_key(self):
        """Generate short key"""
        self.short_key = self.key[:5]
        self.key = hash_api_key(self.key)
        return self
