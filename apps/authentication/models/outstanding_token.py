"""

Outstanding Token Model

This model is used to store the outstanding tokens.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from datetime import datetime
from typing import List
from uuid import UUID

from fastapi_sqlalchemy import db
from pydantic import field_validator
from sqlmodel import Field, Relationship

from apps.authentication.constants.token_constants import TokenTypes
from apps.common.models.base_model import BaseModel
from apps.users.models.user import User


class OutstandingToken(BaseModel, table=True):
    """Outstanding Token Model."""

    __tablename__ = "outstanding_tokens"

    jti: str = Field(..., unique=True, description="JWT ID")
    token_type: str = Field(..., description="Token type")
    expires_at: datetime = Field(..., description="Token expiry time")
    revoked: bool = Field(default=False, description="Is token revoked")
    revoked_at: int = Field(default=None, description="Token revoked time")

    # relationship
    user_id: UUID = Field(foreign_key="users.id")
    user: User = Relationship(back_populates="outstanding_tokens")
    blacklisted_token: List["BlacklistedToken"] = Relationship(
        back_populates="outstanding_token"
    )

    def revoke(self) -> None:
        """Revoke the token."""
        self.revoked = True
        self.revoked_at = datetime.now().timestamp()

    @field_validator("expires_at", mode="after")
    @classmethod
    def validate_expires_at(cls, expires_at: datetime) -> datetime:
        """Validate expires_at."""
        if expires_at < datetime.now():
            raise ValueError("Expiry date should be greater than today.")
        return expires_at

    @field_validator("token_type", mode="after")
    @classmethod
    def validate_token_type(cls, token_type: str) -> str:
        """Validate token_type."""
        if token_type not in TokenTypes.values():
            raise ValueError("Invalid token type.")
        return token_type

    @field_validator("user_id", mode="after")
    @classmethod
    def validate_user_id(cls, user_id: UUID) -> UUID:
        """Validate user_id."""
        if not db.session.query(User).get(user_id):
            raise ValueError(f"User with id '{user_id}' not found.")
        return user_id
