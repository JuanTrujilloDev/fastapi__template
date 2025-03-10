"""

Runserver script for FastAPI application.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import uvicorn

from fastapi__template.settings import settings


def main():
    """Run FastAPI application."""

    uvicorn.run(
        "fastapi__template.app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
