"""
MRGpt Browser

History Repository
"""

from __future__ import annotations

from datetime import datetime

from database.sqlite.sqlite_repository import SQLiteRepository

from models.history_item import HistoryItem


class HistoryRepository(SQLiteRepository):

    """
    History Repository
    """

    # -------------------------------------------------

    @property
    def table(self):

        return "history"
    
    # -------------------------------------------------
    @staticmethod
    def _to_datetime(value) -> datetime:

        if isinstance(value, datetime):
            return value

        if isinstance(value, str) and value:

            return datetime.fromisoformat(value)

        return datetime.now()


    @staticmethod
    def _to_iso(value) -> str:

        if isinstance(value, datetime):
            return value.isoformat()

        if isinstance(value, str):
            return value

        return datetime.now().isoformat()

    # -------------------------------------------------

    def to_record(
    self,
    item: HistoryItem,
) -> dict:

        return {
            "title": item.title,
            "url": item.url,
            "visit_time": self._to_iso(item.visit_time),
            "visit_count": item.visit_count,
            "favicon": item.favicon,
            "created_at": self._to_iso(item.created_at),
            "updated_at": self._to_iso(item.updated_at),
        }
    # -------------------------------------------------

    def from_record(
    self,
    row,
) -> HistoryItem:

        return HistoryItem(
            id=row["id"],
            title=row["title"] or "",
            url=row["url"] or "",
            visit_time=self._to_datetime(
                row["visit_time"]
            ),
            visit_count=row["visit_count"] or 1,
            favicon=row["favicon"] or "",
            created_at=self._to_datetime(
                row["created_at"]
            ),
            updated_at=self._to_datetime(
                row["updated_at"]
            ),
        )
    # -------------------------------------------------

    def add(
    self,
    item: HistoryItem,
) -> int:

        record = self.to_record(item)

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
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["title"],
                record["url"],
                record["visit_time"],
                record["visit_count"],
                record["favicon"],
                record["created_at"],
                record["updated_at"],
            ),
        )

        return cursor.lastrowid
    # -------------------------------------------------

    def update(
    self,
    item: HistoryItem,
) -> bool:

        record = self.to_record(item)
    
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
                record["title"],
                record["url"],
                record["visit_time"],
                record["visit_count"],
                record["favicon"],
                record["updated_at"],
                item.id,
            ),
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