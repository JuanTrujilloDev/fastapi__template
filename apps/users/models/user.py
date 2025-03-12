"""

User Model

This model is used to store the Users.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from typing import List

import bcrypt
from fastapi_sqlalchemy import db
from pydantic import EmailStr, field_validator, model_validator
from pydantic_core import PydanticCustomError
from sqlmodel import Field, Relationship

from apps.authentication.methods.hash_util_methods import (
    hash_string_with_secret_key,
)
from apps.common.models.base_model import BaseModel
from apps.exceptions.constants.error_codes import ErrorCodes


class User(BaseModel, table=True):
    """User model"""

    __tablename__ = "users"

    # TODO: Validate password with regex?
    email: EmailStr = Field(..., description="Email of the user", unique=True)
    password: bytes = Field(..., description="Password of the user")
    password_salt: bytes = Field(
        default_factory=bcrypt.gensalt,
        description="Password salt of the user",
    )
    first_name: str = Field(
        ..., description="First name of the user", min_length=1, max_length=50
    )
    last_name: str = Field(
        ..., description="Last name of the user", min_length=1, max_length=50
    )
    is_staff: bool = Field(default=False, description="Is user staff")
    is_superuser: bool = Field(default=False, description="Is user superuser")

    # relationships
    outstanding_tokens: List["OutstandingToken"] = Relationship(
        back_populates="user", cascade_delete=True
    )

    def __str__(self):
        return self.name

    @model_validator(mode="after")
    def hash_password(self):
        """Hash password and store it with the salt."""
        if not self.password:
            return self

        self.password = hash_string_with_secret_key(
            str(self.password), self.password_salt
        )
        return self

    @field_validator("email", mode="after")
    @classmethod
    def validate_email_repeated(cls, value: EmailStr, values):
        """Validate email is not repeated."""
        if not value:
            return value

        user = (
            db.session.query(User)
            .filter(User.email == value, User.id != values.data.get("id"))
            .first()
        )
        if user:
            raise PydanticCustomError(
                ErrorCodes.DUPLICATE_DATA,
                f"Email {value} already exists",
            )

        return value
