"""

Test setup file for the FastAPI project.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import os

import sqlalchemy as sa

from fastapi__template.dependencies import DEFAULT_ENGINE
from fastapi__template.test.test_constants import TEST_DB_NAME, DBExistsCommand


def prepare_test_database():
    """Prepare test database."""
    connection = DEFAULT_ENGINE.connect()
    connection.execution_options(isolation_level="AUTOCOMMIT")
    exists = connection.execute(
        sa.text(
            DBExistsCommand.get_command(
                os.environ.get("DATABASE_ENGINE", "postgresql")
            ).format(database_name=TEST_DB_NAME)
        )
    ).fetchone()
    if not exists:
        connection.execute(sa.text(f"CREATE DATABASE {TEST_DB_NAME}"))

    connection.commit()
    connection.close()


def drop_test_database():
    """Drop test database."""
    connection = DEFAULT_ENGINE.connect()
    connection.execution_options(isolation_level="AUTOCOMMIT")
    exists = connection.execute(
        sa.text(
            DBExistsCommand.get_command(
                os.environ.get("DATABASE_ENGINE", "postgresql")
            ).format(database_name=TEST_DB_NAME)
        )
    ).fetchone()
    if exists:
        connection.execute(sa.text(f"DROP DATABASE {TEST_DB_NAME} WITH (FORCE)"))

    connection.commit()
    connection.close()
