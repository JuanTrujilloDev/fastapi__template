"""

Database module.

This module is used to set up the database.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

ALLOWED_ENGINES = {
    "sqlite": "sqlite:///./{database_name}.db",
    "postgresql": (
        "postgresql://{database_user}:{database_password}"
        "@{database_host}:{database_port}"
    ),
    "mysql": (
        "mysql://{database_user}:{database_password}@" "{database_host}:{database_port}"
    ),
    "mssql": (
        "mssql://{database_user}:{database_password}@{database_host}:{database_port}",
    ),
    "postgresql+psycopg": (
        "postgresql+psycopg://{database_user}:{database_password}"
        "@{database_host}:{database_port}"
    ),
    "postgresql+psycopg2": (
        "postgresql+psycopg2://{database_user}:{database_password}"
        "@{database_host}:{database_port}"
    ),
}


def get_engine(**kwargs) -> str:
    """Get database engine."""
    try:
        return ALLOWED_ENGINES[kwargs.get("database_engine")].format(**kwargs)
    except KeyError as e:
        raise ValueError(
            f"Engine '{kwargs.get("database_engine")}' not allowed "
            f"allowed are: {list(ALLOWED_ENGINES.keys())}."
        ) from e
