"""

Base model for SQLAlchemy

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import asyncio
import uuid
from datetime import datetime
from typing import Awaitable, Callable, List, Optional

from tortoise import fields, models

CleanMethod = Callable[[], Awaitable[None]]


class BaseModel(models.Model):
    """Base model for all models"""

    id: Optional[uuid.UUID] = fields.UUIDField(
        primary_key=True, nullable=False, default=uuid.uuid4, unique=True
    )
    is_active: Optional[bool] = fields.BooleanField(default=True, nullable=False)
    created_at: datetime = fields.DatetimeField(auto_now_add=True, nullable=False)
    updated_at: datetime = fields.DatetimeField(
        auto_now=True, auto_now_add=True, nullable=False
    )

    class Meta:
        """Meta class for BaseModel"""

        abstract = True
        ordering = ["-updated_at"]

    def __init__(self, *args, **kwargs):
        """Initialize the base model"""
        super().__init__(*args, **kwargs)
        self.clean_methods: List[CleanMethod] = [
            getattr(self, method)
            for method in dir(self)
            if method.startswith("clean_")
            and isinstance(getattr(self, method), CleanMethod)
        ]

    def __str__(self):
        """String representation of the model"""
        return str(self.id)

    async def clean(self):
        """Clean the model"""
        await asyncio.gather(*(method() for method in self.clean_methods))
        return self

    async def save(self, *args, **kwargs):
        """Save the model"""
        await self.clean()
        super().save(*args, **kwargs)
