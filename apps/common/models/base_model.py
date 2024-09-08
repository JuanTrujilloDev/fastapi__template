"""

Base model for SQLAlchemy

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import uuid
from datetime import datetime, timezone
from functools import partial
from typing import Optional

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    """Base model for all models"""

    id: Optional[uuid.UUID] = Field(
        primary_key=True, nullable=False, default_factory=uuid.uuid4, unique=True
    )
    is_active: Optional[bool] = Field(default=True)
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(
        default_factory=partial(datetime.now, tz=timezone.utc), nullable=False
    )

    model_config = ConfigDict(from_attributes=True)

    def __init__(self, **kwargs):
        self.model_config["table"] = False
        super().__init__(**kwargs)
        self.model_config["table"] = True
