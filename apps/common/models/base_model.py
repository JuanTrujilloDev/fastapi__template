"""

Base model for SQLAlchemy

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import uuid
from abc import ABC
from datetime import datetime, timezone
from functools import partial
from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel, ABC):
    """Base model for all models"""

    id: Optional[UUID] = Field(
        default=uuid.uuid4(), primary_key=True, allow_mutation=False
    )
    is_active: Optional[bool] = Field(default=True)
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(
        default_factory=partial(datetime.now, tz=timezone.utc), nullable=False
    )

    class Config:
        validate_assignment = True
