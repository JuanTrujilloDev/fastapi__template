"""

Test setup file for the FastAPI project.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import os

import sqlalchemy as sa

from fastapi__template.database import get_engine
from fastapi__template.settings import SETTINGS

TEST_DB_NAME = SETTINGS.DATABASE_NAME + "_test"
EXISTS_COMMAND = {
    "postgresql": (
        f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'"  # nosec: B608
    ),
    "mysql": (
        "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "  # nosec: B608
        f"WHERE SCHEMA_NAME = '{TEST_DB_NAME}'"  # nosec: B608
    ),
    "mssql": (
        f"SELECT 1 FROM sys.databases WHERE name = '{TEST_DB_NAME}'"  # nosec: B608
    ),
    "postgresql+psycopg": (
        f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'"  # nosec: B608
    ),
    "postgresql+psycopg2": (
        f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'"  # nosec: B608
    ),
}
TEST_DB_ENGINE = get_engine(
    database_engine=SETTINGS.DATABASE_ENGINE_NAME,
    database_name=SETTINGS.DATABASE_NAME,
    database_user=SETTINGS.DATABASE_USER,
    database_password=SETTINGS.DATABASE_PASSWORD,
    database_host=SETTINGS.DATABASE_HOST,
    database_port=SETTINGS.DATABASE_PORT,
)

engine = sa.create_engine(TEST_DB_ENGINE, poolclass=sa.StaticPool)


def prepare_test_database():
    """Prepare test database."""
    connection = engine.connect()
    connection.execution_options(isolation_level="AUTOCOMMIT")
    exists = connection.execute(
        sa.text(
            EXISTS_COMMAND[os.environ.get("DATABASE_ENGINE", "postgresql")].format(
                database_name=TEST_DB_NAME
            )
        )
    ).fetchone()
    if not exists:
        connection.execute(sa.text(f"CREATE DATABASE {TEST_DB_NAME}"))

    connection.commit()
    connection.close()


def drop_test_database():
    """Drop test database."""
    connection = engine.connect()
    connection.execution_options(isolation_level="AUTOCOMMIT")
    exists = connection.execute(
        sa.text(
            EXISTS_COMMAND[os.environ.get("DATABASE_ENGINE", "postgresql")].format(
                database_name=TEST_DB_NAME
            )
        )
    ).fetchone()
    if exists:
        connection.execute(sa.text(f"DROP DATABASE {TEST_DB_NAME} WITH (FORCE)"))

    connection.commit()
    connection.close()
