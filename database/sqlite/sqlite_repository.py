"""
MRGpt Browser

SQLite Repository
"""

from __future__ import annotations

import sqlite3

from abc import abstractmethod

from database.repository.base_repository import BaseRepository


class SQLiteRepository(BaseRepository):

    """
    Base SQLite Repository
    """

    # -------------------------------------------------

    def __init__(

        self,

        connection: sqlite3.Connection,

    ):

        self.connection = connection

        self.cursor = connection.cursor()

    # -------------------------------------------------

    @property
    @abstractmethod
    def table(self) -> str:

        """
        Database table name.
        """

        ...

    # -------------------------------------------------

    @abstractmethod
    def to_record(self, item):

        """
        Model -> dict
        """

        ...

    # -------------------------------------------------

    @abstractmethod
    def from_record(self, row):

        """
        sqlite row -> Model
        """

        ...

    # -------------------------------------------------

    def execute(

        self,

        sql,

        parameters=(),

    ):

        self.cursor.execute(

            sql,

            parameters

        )

        self.connection.commit()

        return self.cursor

    # -------------------------------------------------

    def executemany(

        self,

        sql,

        values,

    ):

        self.cursor.executemany(

            sql,

            values

        )

        self.connection.commit()

    # -------------------------------------------------

    def get(

        self,

        item_id,

    ):

        row = self.execute(

            f"""

            SELECT *

            FROM {self.table}

            WHERE id=?

            """,

            (item_id,)

        ).fetchone()

        if row is None:

            return None

        return self.from_record(row)

    # -------------------------------------------------

    def all(self):

        rows = self.execute(

            f"""

            SELECT *

            FROM {self.table}

            ORDER BY id

            """

        ).fetchall()

        return [

            self.from_record(row)

            for row in rows

        ]

    # -------------------------------------------------

    def exists(

        self,

        item_id,

    ):

        row = self.execute(

            f"""

            SELECT 1

            FROM {self.table}

            WHERE id=?

            """,

            (item_id,)

        ).fetchone()

        return row is not None

    # -------------------------------------------------

    def count(self):

        row = self.execute(

            f"""

            SELECT COUNT(*)

            FROM {self.table}

            """

        ).fetchone()

        return row[0]

    # -------------------------------------------------

    def clear(self):

        self.execute(

            f"""

            DELETE FROM {self.table}

            """

        )

    # -------------------------------------------------

    def delete(

        self,

        item_id,

    ):

        self.execute(

            f"""

            DELETE

            FROM {self.table}

            WHERE id=?

            """,

            (item_id,)

        )

        return True