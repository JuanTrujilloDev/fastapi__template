"""
Migration script for the database.

This script is used to migrate the database.


This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import alembic
from alembic.config import Config as AlembicConfig

from fastapi__template.app import create_app

# init app
app = create_app()
app.dependency_overrides = {}


def main():
    """Migrate the database."""
    alembic_cfg = AlembicConfig("fastapi__template/migrations/alembic.ini")
    alembic.command.upgrade(alembic_cfg, "head")
