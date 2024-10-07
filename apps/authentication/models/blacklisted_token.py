"""

BlacklistedToken Model

This model is used to store the blacklisted tokens.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from uuid import UUID

from fastapi_sqlalchemy import db
from pydantic import field_validator
from sqlmodel import Field, Relationship

from apps.authentication.models.outstanding_token import OutstandingToken
from apps.common.models.base_model import BaseModel


class BlacklistedToken(BaseModel, table=True):
    """Blacklisted Token Model."""

    __tablename__ = "blacklisted_tokens"

    # relationship
    outstanding_token_id: UUID = Field(..., foreign_key="outstanding_tokens.id")
    outstanding_token: OutstandingToken = Relationship(back_populates="blacklisted_token")

    @field_validator("outstanding_token_id", mode="after")
    @classmethod
    def validate_outstanding_token_id(cls, outstanding_token_id: UUID) -> UUID:
        """Validate outstanding_token_id."""
        if not db.session.get(OutstandingToken, outstanding_token_id):
            raise ValueError("Invalid outstanding token id.")
        return outstanding_token_id
