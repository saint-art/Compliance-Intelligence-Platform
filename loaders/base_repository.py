from abc import ABC, abstractmethod
import sqlite3

from database.database_manager import DatabaseManager
from utils.logger import get_logger


class BaseRepository(ABC):
    """
    Base repository for database persistence.

    Provides:

    - SQLite connection
    - shared cursor
    - commit / rollback helpers
    - repository logger
    - connection cleanup

    A repository may either:

    1. receive an existing connection from the application/pipeline, or
    2. create its own connection when used independently.

    When repositories share an injected connection, they also share
    the same transaction boundary.
    """

    def __init__(
        self,
        connection: sqlite3.Connection = None
    ):

        self._owns_connection = connection is None

        if connection is None:

            self.connection = (
                DatabaseManager.connect()
            )

        else:

            self.connection = connection

        self.cursor = self.connection.cursor()

        self.logger = get_logger(
            self.__class__.__name__
        )

    # ---------------------------------------------------------
    # TRANSACTION CONTROL
    # ---------------------------------------------------------

    def commit(self):
        """
        Commit the current transaction.

        Transaction control should normally happen at the
        application/pipeline boundary rather than inside
        individual repository operations.
        """

        if self.connection is None:

            raise RuntimeError(
                "Cannot commit: repository connection is closed."
            )


    def rollback(self):
        """
        Roll back the current transaction.
        """

        if self.connection is None:

            raise RuntimeError(
                "Cannot rollback: repository connection is closed."
            )


    # ---------------------------------------------------------
    # CONNECTION MANAGEMENT
    # ---------------------------------------------------------

    def close(self):
        """
        Close the repository.

        A repository only closes a connection if it created
        that connection itself.

        Shared/injected connections remain owned by the caller.
        """

        if self.cursor is not None:

            self.cursor.close()

        self.cursor = None

        if (
            self.connection is not None
            and self._owns_connection
        ):

            self.connection.close()

        self.connection = None

    # ---------------------------------------------------------
    # ABSTRACT REPOSITORY CONTRACT
    # ---------------------------------------------------------

    @abstractmethod
    def save(self, entity):
        pass

    @abstractmethod
    def save_many(self, entities):
        pass
