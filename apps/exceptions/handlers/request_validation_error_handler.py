"""

Request validation error handler.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def request_validation_error_handler(request: Request, exc: RequestValidationError):
    """
    Request validation error handler.
    """
    errors = exc.errors()

    request_json = await request.json()
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": errors, "body": request_json}),
    )
