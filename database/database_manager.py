from pathlib import Path
import sqlite3

from utils.logger import get_logger


logger = get_logger("DatabaseManager")


class DatabaseManager:
    """
    Centralized SQLite database connection and initialization manager.

    Responsibilities:

    - Maintain canonical database and schema paths.
    - Initialize the database schema.
    - Create configured SQLite connections.
    - Enable foreign-key enforcement on every connection.

    Transaction ownership does NOT belong here.

    The caller that owns a connection is responsible for:
        connection.commit()
        connection.rollback()
        connection.close()
    """

    DATABASE_PATH = Path("database/compliance.db")
    SCHEMA_PATH = Path("database/schema.sql")

    @classmethod
    def initialize(cls):
        """
        Initialize the SQLite database using the canonical schema.

        Safe to call repeatedly because the schema uses
        CREATE TABLE IF NOT EXISTS and CREATE INDEX IF NOT EXISTS.
        """

        cls.DATABASE_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        first_time = not cls.DATABASE_PATH.exists()

        connection = sqlite3.connect(
            cls.DATABASE_PATH
        )

        try:

            connection.execute(
                "PRAGMA foreign_keys = ON"
            )

            with open(
                cls.SCHEMA_PATH,
                "r",
                encoding="utf-8"
            ) as schema:

                connection.executescript(
                    schema.read()
                )

            connection.commit()

            if first_time:

                logger.info(
                    "Database created successfully."
                )

            else:

                logger.info(
                    "Database schema verified."
                )

        except Exception:

            connection.rollback()

            logger.exception(
                "Database initialization failed."
            )

            raise

        finally:

            connection.close()

    @classmethod
    def connect(cls):
        """
        Create and return a configured SQLite connection.

        The connection uses:

        - sqlite3.Row for named column access.
        - DEFERRED transaction mode.
        - foreign-key enforcement.

        This method does not commit or rollback anything.
        Transaction ownership belongs to the caller.
        """

        if not cls.DATABASE_PATH.exists():

            cls.initialize()

        connection = sqlite3.connect(
            cls.DATABASE_PATH,
            isolation_level="DEFERRED"
        )

        connection.row_factory = sqlite3.Row

        # SQLite foreign-key enforcement is connection-specific.
        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return connection