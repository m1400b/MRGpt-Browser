"""
MRGpt Browser

Bookmark Repository
"""

from __future__ import annotations

from datetime import datetime

from database.model_mapper import ModelMapper
from database.sqlite.sqlite_repository import SQLiteRepository

from models.bookmark_item import BookmarkItem


class BookmarkRepository(SQLiteRepository[BookmarkItem]):

    """
    Bookmark Repository
    """

    # -------------------------------------------------

    @property
    def table(self) -> str:

        return "bookmarks"

    # -------------------------------------------------

    def to_record(
        self,
        item: BookmarkItem,
    ) -> dict:

        return ModelMapper.to_record(item)

    # -------------------------------------------------

    def from_record(
        self,
        row,
    ) -> BookmarkItem:

        return ModelMapper.from_record(
            BookmarkItem,
            row,
        )

    # -------------------------------------------------

    def add(
        self,
        item: BookmarkItem,
    ) -> int:

        cursor = self.execute(

            f"""
            INSERT INTO {self.table}
            (
                title,
                url,
                folder,
                description,
                favorite,
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
                item.folder,
                item.description,
                int(item.favorite),
                item.created_at,
                item.updated_at,
            ),
        )

        return cursor.lastrowid

    # -------------------------------------------------

    def update(
        self,
        item: BookmarkItem,
    ) -> bool:

        self.execute(

            f"""
            UPDATE {self.table}
            SET
                title=?,
                url=?,
                folder=?,
                description=?,
                favorite=?,
                updated_at=?
            WHERE id=?
            """,

            (
                item.title,
                item.url,
                item.folder,
                item.description,
                int(item.favorite),
                datetime.now().isoformat(),
                item.id,
            ),
        )

        return True

    # -------------------------------------------------

    def find_by_url(
        self,
        url: str,
    ) -> BookmarkItem | None:

        row = self.execute(

            f"""
            SELECT *
            FROM {self.table}
            WHERE url=?
            LIMIT 1
            """,

            (url,),
        ).fetchone()

        if row is None:

            return None

        return self.from_record(row)

    # -------------------------------------------------

    def search(
        self,
        keyword: str,
    ) -> list[BookmarkItem]:

        rows = self.execute(

            f"""
            SELECT *
            FROM {self.table}
            WHERE
                title LIKE ?
                OR
                url LIKE ?
                OR
                folder LIKE ?
            ORDER BY title
            """,

            (
                f"%{keyword}%",
                f"%{keyword}%",
                f"%{keyword}%",
            ),
        ).fetchall()

        return [

            self.from_record(row)

            for row in rows

        ]

    # -------------------------------------------------

    def favorites(
        self,
    ) -> list[BookmarkItem]:

        rows = self.execute(

            f"""
            SELECT *
            FROM {self.table}
            WHERE favorite=1
            ORDER BY title
            """

        ).fetchall()

        return [

            self.from_record(row)

            for row in rows

        ]

    # -------------------------------------------------

    def find_by_folder(
        self,
        folder: str,
    ) -> list[BookmarkItem]:

        rows = self.execute(

            f"""
            SELECT *
            FROM {self.table}
            WHERE folder=?
            ORDER BY title
            """,

            (folder,),
        ).fetchall()

        return [

            self.from_record(row)

            for row in rows

        ]

    # -------------------------------------------------

    def rename_folder(
        self,
        old_name: str,
        new_name: str,
    ) -> None:

        self.execute(

            f"""
            UPDATE {self.table}
            SET
                folder=?,
                updated_at=?
            WHERE folder=?
            """,

            (
                new_name,
                datetime.now().isoformat(),
                old_name,
            ),
        )

    # -------------------------------------------------

    def delete_folder(
        self,
        folder: str,
    ) -> None:

        self.execute(

            f"""
            DELETE
            FROM {self.table}
            WHERE folder=?
            """,

            (folder,),
        )

    # -------------------------------------------------

    def exists_url(
        self,
        url: str,
    ) -> bool:

        row = self.execute(

            f"""
            SELECT 1
            FROM {self.table}
            WHERE url=?
            LIMIT 1
            """,

            (url,),
        ).fetchone()

        return row is not None