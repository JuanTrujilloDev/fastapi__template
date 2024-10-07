"""

Token constants

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from enum import StrEnum


class TokenTypes(StrEnum):
    """Token Types."""

    ACCESS = "access"
    REFRESH = "refresh"

    @staticmethod
    def values():
        return TokenTypes._value2member_map_
