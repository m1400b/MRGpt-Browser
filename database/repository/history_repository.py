"""
MRGpt Browser

History Repository
"""

from __future__ import annotations

from datetime import datetime

from database.sqlite.sqlite_repository import SQLiteRepository

from models.history_item import HistoryItem


class HistoryRepository(SQLiteRepository[HistoryItem]):

    """
    History Repository
    """

    # -------------------------------------------------

    @property
    def table(self):

        return "history"

    # -------------------------------------------------

    def to_record(
        self,
        item: HistoryItem
    ) -> dict:

        return {

            "title": item.title,

            "url": item.url,

            "visit_time": item.visit_time,

            "visit_count": item.visit_count,

            "favicon": item.favicon,

            "created_at": item.created_at,

            "updated_at": item.updated_at,

        }

    # -------------------------------------------------

    def from_record(
        self,
        row
    ) -> HistoryItem:

        item = HistoryItem()

        item.id = row["id"]

        item.title = row["title"]

        item.url = row["url"]

        item.visit_time = row["visit_time"]

        item.visit_count = row["visit_count"]

        item.favicon = row["favicon"]

        item.created_at = row["created_at"]

        item.updated_at = row["updated_at"]

        return item

    # -------------------------------------------------

    def add(
        self,
        item: HistoryItem
    ) -> int:

        cursor = self.execute(

            f"""
            INSERT INTO {self.table}

            (
                title,
                url,
                visit_time,
                visit_count,
                favicon,
                created_at,
                updated_at
            )

            VALUES
            (
                ?,?,?,?,?,?,?
            )
            """,

            (

                item.title,

                item.url,

                item.visit_time,

                item.visit_count,

                item.favicon,

                item.created_at,

                item.updated_at,

            )

        )

        return cursor.lastrowid

    # -------------------------------------------------

    def update(
        self,
        item: HistoryItem
    ) -> bool:

        self.execute(

            f"""
            UPDATE {self.table}

            SET

                title=?,

                url=?,

                visit_time=?,

                visit_count=?,

                favicon=?,

                updated_at=?

            WHERE id=?
            """,

            (

                item.title,

                item.url,

                item.visit_time,

                item.visit_count,

                item.favicon,

                datetime.now().isoformat(),

                item.id,

            )

        )

        return True

    # -------------------------------------------------

    def find_by_url(
        self,
        url: str
    ) -> HistoryItem | None:

        row = self.execute(

            f"""
            SELECT *

            FROM {self.table}

            WHERE url=?

            LIMIT 1
            """,

            (url,)

        ).fetchone()

        if row is None:

            return None

        return self.from_record(row)

    # -------------------------------------------------

    def search(
        self,
        keyword: str
    ) -> list[HistoryItem]:

        rows = self.execute(

            f"""
            SELECT *

            FROM {self.table}

            WHERE

                title LIKE ?

                OR

                url LIKE ?

            ORDER BY visit_time DESC
            """,

            (

                f"%{keyword}%",

                f"%{keyword}%",

            )

        ).fetchall()

        return [

            self.from_record(row)

            for row in rows

        ]

    # -------------------------------------------------

    def last_visited(
        self,
        limit: int = 50
    ) -> list[HistoryItem]:

        rows = self.execute(

            f"""
            SELECT *

            FROM {self.table}

            ORDER BY visit_time DESC

            LIMIT ?
            """,

            (limit,)

        ).fetchall()

        return [

            self.from_record(row)

            for row in rows

        ]

    # -------------------------------------------------

    def delete_by_url(
        self,
        url: str
    ):

        self.execute(

            f"""
            DELETE

            FROM {self.table}

            WHERE url=?
            """,

            (url,)

        )