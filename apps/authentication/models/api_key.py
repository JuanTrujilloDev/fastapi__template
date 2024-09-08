"""

API Key Model

This model is used to store the API keys for the users.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from datetime import date, datetime

from tortoise import fields

from apps.authentication.methods.api_key_util_methods import hash_api_key
from apps.common.models.base_model import BaseModel


class APIKey(BaseModel):
    """API Key model"""

    key: bytes = fields.BinaryField(null=False, unique=True, description="API key")
    short_key: str = fields.CharField(
        max_length=5, null=True, unique=True, description="Short key"
    )
    title: str = fields.CharField(max_length=255, null=False, description="Title")
    description: str = fields.TextField(null=True, description="Description")
    expiry_date: date = fields.DatetimeField(null=True, description="Expiry date")

    @property
    def enabled(self):
        """
        Check if the API key is enabled to use.
        """
        if not self.expiry_date:
            return self.is_active
        return self.expiry_date > datetime.now() and self.is_active

    async def clean_expiry_date(self):
        """Validate expiry date"""
        if self.expiry_date and self.expiry_date() < datetime.now().date():
            raise ValueError("Expiry date should be greater than today.")

    async def save(self, *args, **kwargs):
        """Save the model"""
        self.short_key = self.key[:5]
        self.key = hash_api_key(self.key)
        super().save(*args, **kwargs)
