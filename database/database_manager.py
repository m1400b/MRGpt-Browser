"""
MRGpt Browser

Database Manager
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


class DatabaseManager:
    """
    SQLite Database Manager
    """

    def __init__(self, database_path: str):

        self.database_path = Path(database_path)

        self.connection: sqlite3.Connection | None = None

    # -------------------------------------------------

    def connect(self):

        """
        Open database connection.
        """

        if self.connection:

            return self.connection

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            self.database_path
        )

        self.connection.row_factory = sqlite3.Row

        self._configure()

        return self.connection

    # -------------------------------------------------

    def _configure(self):

        """
        SQLite configuration.
        """

        cursor = self.connection.cursor()

        cursor.execute(
            "PRAGMA foreign_keys = ON"
        )

        cursor.execute(
            "PRAGMA journal_mode = WAL"
        )

        cursor.execute(
            "PRAGMA synchronous = NORMAL"
        )

        cursor.execute(
            "PRAGMA temp_store = MEMORY"
        )

        cursor.execute(
            "PRAGMA cache_size = -10000"
        )

        self.connection.commit()

    # -------------------------------------------------

    def cursor(self):

        if self.connection is None:

            self.connect()

        return self.connection.cursor()

    # -------------------------------------------------

    def commit(self):

        if self.connection:

            self.connection.commit()

    # -------------------------------------------------

    def rollback(self):

        if self.connection:

            self.connection.rollback()

    # -------------------------------------------------

    def close(self):

        if self.connection:

            self.connection.close()

            self.connection = None

    # -------------------------------------------------

    def execute(
        self,
        sql,
        parameters=()
    ):

        cursor = self.cursor()

        cursor.execute(
            sql,
            parameters
        )

        self.commit()

        return cursor

    # -------------------------------------------------

    def executemany(
        self,
        sql,
        values
    ):

        cursor = self.cursor()

        cursor.executemany(
            sql,
            values
        )

        self.commit()

        return cursor