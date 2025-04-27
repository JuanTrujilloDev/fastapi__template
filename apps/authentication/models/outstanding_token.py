"""

Outstanding Token Model

This model is used to store the outstanding tokens.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from datetime import datetime, timezone
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
    client: str = Field(..., description="Client ID")
    token_type: TokenTypes = Field(..., description="Token type")
    expires_at: datetime = Field(..., description="Token expiry time")
    revoked: bool = Field(default=False, description="Is token revoked")

    # relationship
    user_id: UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    user: User = Relationship(back_populates="outstanding_tokens")

    @property
    def is_valid(self) -> bool:
        """Check if the token is valid."""
        return (
            not self.revoked
            and self.expires_at > datetime.now(tz=timezone.utc)
            and self.is_active
        )

    def revoke(self) -> None:
        """Revoke the token."""
        self.revoked = True

    @field_validator("expires_at", mode="after")
    @classmethod
    def validate_expires_at(cls, expires_at: datetime) -> datetime:
        """Validate expires_at."""
        if expires_at < datetime.now(tz=timezone.utc):
            raise ValueError("Expiry date should be greater than today.")
        return expires_at

    @field_validator("user_id", mode="after")
    @classmethod
    def validate_user_id(cls, user_id: UUID) -> UUID:
        """Validate user_id."""
        if not db.session.query(User).get(user_id):
            raise ValueError(f"User with id '{user_id}' not found.")
        return user_id
