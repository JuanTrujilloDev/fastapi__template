"""

User Model

This model is used to store the Users.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from datetime import datetime, timezone

from pydantic import EmailStr, model_validator
from sqlmodel import Field

from apps.authentication.methods.password_util_methods import (
    hash_password_with_secret_key,
)
from apps.common.models.base_model import BaseModel


class User(BaseModel, table=True):
    """User model"""

    __tablename__ = "users"

    # TODO: Validate password
    email: EmailStr = Field(..., description="Email of the user", unique=True)
    password: str = Field(..., description="Password of the user")
    first_name: str = Field(
        ..., description="First name of the user", min_length=1, max_length=50
    )
    last_name: str = Field(
        ..., description="Last name of the user", min_length=1, max_length=50
    )
    is_staff: bool = Field(default=False, description="Is user staff")
    is_superuser: bool = Field(default=False, description="Is user superuser")
    date_joined: datetime = Field(default=datetime.now(timezone.utc), nullable=False)

    def __str__(self):
        return self.name

    @model_validator(mode="after")
    def hash_password(self):
        """Hash password before saving"""
        self.password = hash_password_with_secret_key(self.password)
        return self
