"""

Base model for SQLAlchemy

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import uuid
from abc import ABC
from datetime import datetime, timezone
from functools import partial
from typing import Any, Optional
from uuid import UUID

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel, ABC):
    """Base model for all models"""

    id: Optional[UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True, allow_mutation=False
    )
    is_active: Optional[bool] = Field(default=True)
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(
        default_factory=partial(datetime.now, tz=timezone.utc), nullable=False
    )

    model_config = ConfigDict(
        from_attributes=True, validate_default=True, validate_assignment=True
    )

    def _set_skip_validation(self, name: str, value: Any) -> None:
        """Workaround to be able to set fields without validation."""
        attr = getattr(self.__class__, name, None)
        if isinstance(attr, property):
            attr.__set__(self, value)
        else:
            self.__dict__[name] = value
            self.__pydantic_fields_set__.add(name)
