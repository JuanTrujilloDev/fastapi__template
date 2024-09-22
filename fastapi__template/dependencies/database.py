"""

Database module.

This module is used to set up the database.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""


class AllowedEngines:
    """Allowed database engines."""

    SQLITE = "sqlite:///./{database_name}.db"  # nosec
    POSTGRESQL = (  # nosec
        "postgresql://{database_user}:{database_password}"
        "@{database_host}:{database_port}"
    )
    MYSQL = (  # nosec
        "mysql://{database_user}:{database_password}@{database_host}:{database_port}"
    )
    MSSQL = (  # nosec
        "mssql://{database_user}:{database_password}@{database_host}:{database_port}",
    )
    POSTGRESQL_PSYCOPG = (  # nosec
        "postgresql+psycopg://{database_user}:{database_password}"
        "@{database_host}:{database_port}"
    )
    POSTGRESQL_PSYCOPG2 = (  # nosec
        "postgresql+psycopg2://{database_user}:{database_password}"
        "@{database_host}:{database_port}"
    )

    @classmethod
    def get_engine(cls, **kwargs) -> str:
        """Get database engine."""
        try:
            return getattr(cls, kwargs.get("database_engine")).format(**kwargs)
        except AttributeError as e:
            raise ValueError(
                f"Engine '{kwargs.get("database_engine")}' not allowed "
                f"allowed are: {list(cls.__dict__.keys())}."
            ) from e
