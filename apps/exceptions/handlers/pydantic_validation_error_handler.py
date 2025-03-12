"""
Handle Pydantic validation errors.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError


async def pydantic_validation_error_handler(request: Request, exc: ValidationError):
    """
    Pydantic validation error handler.
    """
    request_json = await request.json() if await request.body() else None
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": exc.errors(), "body": request_json}),
    )
