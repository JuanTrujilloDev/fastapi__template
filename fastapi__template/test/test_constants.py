"""

Test constants, such as test database name and test database engine,
are defined in this file.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from enum import StrEnum

from fastapi__template.dependencies.database import AllowedEngines
from fastapi__template.settings import SETTINGS

TEST_DB_NAME = SETTINGS.DATABASE_NAME + "_test"


class DBExistsCommand(StrEnum):
    """

    Enum for database exists command.

    Attributes:
        postgresql: PostgreSQL database exists command.
        mysql: MySQL database exists command.
        mssql: Microsoft SQL Server database exists command.
        postgresql_psycopg: PostgreSQL database exists command for psycopg.
        postgresql_psycopg2: PostgreSQL database exists command for psycopg
    """

    POSTGRESQL = f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'"  # nosec
    MYSQL = (
        "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "  # nosec
        f"WHERE SCHEMA_NAME = '{TEST_DB_NAME}'"
    )
    MSSQL = f"SELECT 1 FROM sys.databases WHERE name = '{TEST_DB_NAME}'"  # nosec
    POSTGRESQL_PSYCOPG = (
        f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'"  # nosec
    )
    POSTGRESQL_PSYCOPG2 = (
        f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'"  # nosec
    )

    @classmethod
    def get_command(cls, database_name: str) -> str:
        """
        Get database exists command.
        """
        try:
            return cls[database_name.upper()].value
        except (KeyError, AttributeError) as error:
            raise ValueError(f"Invalid database engine {database_name}") from error


TEST_DB_ENGINE = AllowedEngines.get_engine(
    database_engine=SETTINGS.DATABASE_ENGINE_NAME,
    database_name=SETTINGS.DATABASE_NAME,
    database_user=SETTINGS.DATABASE_USER,
    database_password=SETTINGS.DATABASE_PASSWORD,
    database_host=SETTINGS.DATABASE_HOST,
    database_port=SETTINGS.DATABASE_PORT,
)
