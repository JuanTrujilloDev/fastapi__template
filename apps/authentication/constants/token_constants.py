"""

Token constants

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from enum import StrEnum

from fastapi.security import OAuth2PasswordBearer


class TokenTypes(StrEnum):
    """Token Types."""

    ACCESS = "access"
    REFRESH = "refresh"


OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/login/")
