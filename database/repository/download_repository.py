"""
MRGpt Browser

Download Repository
"""

from __future__ import annotations

from datetime import datetime

from database.model_mapper import ModelMapper
from database.sqlite.sqlite_repository import SQLiteRepository

from models.download_item import DownloadItem


class DownloadRepository(SQLiteRepository[DownloadItem]):

    """
    Download Repository
    """

    # -------------------------------------------------

    @property
    def table(self) -> str:

        return "downloads"

    # -------------------------------------------------

    def to_record(
        self,
        item: DownloadItem,
    ) -> dict:

        return ModelMapper.to_record(item)

    # -------------------------------------------------

    def from_record(
        self,
        row,
    ) -> DownloadItem:

        return ModelMapper.from_record(
            DownloadItem,
            row,
        )

    # -------------------------------------------------

    def add(
        self,
        item: DownloadItem,
    ) -> int:

        cursor = self.execute(

            f"""
            INSERT INTO {self.table}
            (
                url,
                file_name,
                save_path,
                mime_type,
                total_bytes,
                received_bytes,
                state,
                created_at,
                updated_at
            )
            VALUES
            (
                ?,?,?,?,?,?,?,?,?
            )
            """,

            (
                item.url,
                item.file_name,
                item.save_path,
                item.mime_type,
                item.total_bytes,
                item.received_bytes,
                item.state,
                item.created_at,
                item.updated_at,
            ),
        )

        return cursor.lastrowid

    # -------------------------------------------------

    def update(
        self,
        item: DownloadItem,
    ) -> bool:

        self.execute(

            f"""
            UPDATE {self.table}
            SET
                url=?,
                file_name=?,
                save_path=?,
                mime_type=?,
                total_bytes=?,
                received_bytes=?,
                state=?,
                updated_at=?
            WHERE id=?
            """,

            (
                item.url,
                item.file_name,
                item.save_path,
                item.mime_type,
                item.total_bytes,
                item.received_bytes,
                item.state,
                datetime.now().isoformat(),
                item.id,
            ),
        )

        return True

    # -------------------------------------------------

    def find_by_url(
        self,
        url: str,
    ) -> DownloadItem | None:

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

    def active_downloads(
        self,
    ) -> list[DownloadItem]:

        rows = self.execute(

            f"""
            SELECT *
            FROM {self.table}
            WHERE state IN
            (
                'queued',
                'downloading',
                'paused'
            )
            ORDER BY created_at DESC
            """

        ).fetchall()

        return [

            self.from_record(row)

            for row in rows

        ]

    # -------------------------------------------------

    def completed_downloads(
        self,
    ) -> list[DownloadItem]:

        rows = self.execute(

            f"""
            SELECT *
            FROM {self.table}
            WHERE state='completed'
            ORDER BY updated_at DESC
            """

        ).fetchall()

        return [

            self.from_record(row)

            for row in rows

        ]

    # -------------------------------------------------

    def failed_downloads(
        self,
    ) -> list[DownloadItem]:

        rows = self.execute(

            f"""
            SELECT *
            FROM {self.table}
            WHERE state='failed'
            ORDER BY updated_at DESC
            """

        ).fetchall()

        return [

            self.from_record(row)

            for row in rows

        ]

    # -------------------------------------------------

    def clear_completed(
        self,
    ) -> None:

        self.execute(

            f"""
            DELETE
            FROM {self.table}
            WHERE state='completed'
            """
        )

    # -------------------------------------------------

    def clear_failed(
        self,
    ) -> None:

        self.execute(

            f"""
            DELETE
            FROM {self.table}
            WHERE state='failed'
            """
        )

    # -------------------------------------------------

    def delete_by_path(
        self,
        path: str,
    ) -> None:

        self.execute(

            f"""
            DELETE
            FROM {self.table}
            WHERE save_path=?
            """,

            (path,),
        )

    # -------------------------------------------------

    def exists_path(
        self,
        path: str,
    ) -> bool:

        row = self.execute(

            f"""
            SELECT 1
            FROM {self.table}
            WHERE save_path=?
            LIMIT 1
            """,

            (path,),
        ).fetchone()

        return row is not None

    # -------------------------------------------------

    def total_download_size(
        self,
    ) -> int:

        row = self.execute(

            f"""
            SELECT
                SUM(total_bytes)
            FROM {self.table}
            WHERE state='completed'
            """

        ).fetchone()

        if row is None:

            return 0

        return row[0] or 0

    # -------------------------------------------------

    def update_progress(
        self,
        item_id: int,
        received_bytes: int,
        state: str,
    ) -> None:

        self.execute(

            f"""
            UPDATE {self.table}
            SET
                received_bytes=?,
                state=?,
                updated_at=?
            WHERE id=?
            """,

            (
                received_bytes,
                state,
                datetime.now().isoformat(),
                item_id,
            ),
        )