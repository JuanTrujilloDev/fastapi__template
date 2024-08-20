"""

Base model for SQLAlchemy

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import uuid
from abc import ABC
from typing import Optional
from uuid import UUID

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel, ABC):
    """Base model for all models"""

    id: Optional[UUID] = Field(
        default=uuid.uuid4(), primary_key=True, allow_mutation=False
    )
    is_active: Optional[bool] = Field(default=True)
    created_at: Optional[str] = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        ),
        allow_mutation=False,
    )
    updated_at: Optional[str] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
        allow_mutation=False,
    )
