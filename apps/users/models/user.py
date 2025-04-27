"""

User Model

This model is used to store the Users.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import re
from typing import List

from fastapi_sqlalchemy import db
from pydantic import EmailStr, field_validator, model_validator
from pydantic_core import PydanticCustomError
from sqlmodel import Field, Relationship

from apps.authentication.methods.hash_util_methods import (
    hash_string,
    verify_strings,
)
from apps.common.models.base_model import BaseModel
from apps.exceptions.constants.error_codes import ErrorCodes
from fastapi__template.settings import settings


class User(BaseModel, table=True):
    """User model"""

    __tablename__ = "users"

    email: EmailStr = Field(..., description="Email of the user", unique=True)
    password: str = Field(
        ...,
        description="Password of the user",
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
        return f"{self.first_name} {self.last_name}"

    def validate_password(self, password: str) -> bool:
        """Validate password."""
        return verify_strings(self.password, password)

    @model_validator(mode="after")
    def hash_password(self):
        """Hash password and store it with the salt."""
        if not self.password:
            return self

        self.password = hash_string(self.password)
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

    @field_validator("password", mode="before")
    @classmethod
    def validate_password_regex(cls, value: str):
        """Validate password."""
        if not isinstance(value, str):
            return value

        if not re.match(settings.PASSWORD_REGEX, value):
            raise PydanticCustomError(
                ErrorCodes.INVALID_DATA,
                "Password must be between 8 and 16 characters long,"
                " contain at least one uppercase letter, one lowercase letter, "
                "one number, and one special character.",
            )

        return value
