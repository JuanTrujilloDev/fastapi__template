from fastapi import HTTPException
from fastapi_sqlalchemy import db
from pydantic import BaseModel

from apps.authentication.constants.token_constants import TokenTypes
from apps.authentication.methods.token_util_methods import create_access_token
from apps.authentication.models.outstanding_token import OutstandingToken


class RefreshTokenSchema(BaseModel):
    """
    Refresh token schema.
    """

    refresh_token: str

    def refresh_access_token(self):
        """Refresh access token."""
        token = self.validate_refresh_token_is_valid()
        db.session.query(OutstandingToken).filter_by(
            user_id=token.user_id, token_type=TokenTypes.ACCESS
        ).update({OutstandingToken.revoked: True})
        db.session.commit()
        access_token = create_access_token(
            {"email": token.user.email},
            token.user_id,
        )
        return access_token

    def validate_refresh_token_is_valid(self):
        """Validate refresh token."""
        token = (
            db.session.query(OutstandingToken)
            .filter_by(jti=self.refresh_token, token_type=TokenTypes.REFRESH)
            .first()
        )
        if not token or not token.is_valid() or not token.user.is_active:
            raise HTTPException(status_code=403, detail="Invalid refresh token")

        return token
