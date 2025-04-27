from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm


class OAuth2EmailPasswordRequestForm(OAuth2PasswordRequestForm):
    """Custom OAuth2 request form that uses email and password."""

    def __init__(
        self,
        *,
        grant_type: Optional[str] = None,
        email: str,
        password: str,
        scope: str = "",
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ):
        self.grant_type = grant_type
        self.username = email
        self.email = email
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret
