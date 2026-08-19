"""
MRGpt Browser

Download Repository
"""

from __future__ import annotations

from datetime import datetime

from database.sqlite.sqlite_repository import SQLiteRepository

from models.download_item import DownloadItem


class DownloadRepository(
    SQLiteRepository
):

    """
    Repository for browser downloads.

    Responsible for persistent storage of
    DownloadItem objects.
    """

    # =================================================
    # Table
    # =================================================

    @property
    def table(self) -> str:

        return "downloads"

    # =================================================
    # Conversion
    # =================================================

    def to_record(
        self,
        item: DownloadItem,
    ) -> dict:

        return {

            "uuid":
                item.uuid,

            "filename":
                item.filename,

            "url":
                item.url,

            "directory":
                item.directory,

            "mime_type":
                item.mime_type,

            "total_bytes":
                item.total_bytes,

            "received_bytes":
                item.received_bytes,

            "progress":
                item.progress,

            "speed":
                item.speed,

            "remaining_seconds":
                item.remaining_seconds,

            "state":
                item.state,

            "paused":
                int(item.paused),

            "finished":
                int(item.finished),

            "successful":
                int(item.successful),

            "canceled":
                int(item.canceled),

            "interrupted":
                int(item.interrupted),

            "started_at":
                self._datetime_to_string(
                    item.started_at
                ),

            "finished_at":
                self._datetime_to_string(
                    item.finished_at
                ),

            "created_at":
                self._datetime_to_string(
                    item.created_at
                ),

            "updated_at":
                self._datetime_to_string(
                    item.updated_at
                ),

            "is_deleted":
                int(item.is_deleted),

        }

    # -------------------------------------------------

    def from_record(
        self,
        row,
    ) -> DownloadItem | None:

        if row is None:

            return None

        return DownloadItem(

            id=row["id"],

            uuid=row["uuid"],

            filename=row["filename"] or "",

            url=row["url"] or "",

            directory=row["directory"] or "",

            mime_type=row["mime_type"] or "",

            total_bytes=
                row["total_bytes"] or 0,

            received_bytes=
                row["received_bytes"] or 0,

            progress=
                row["progress"] or 0.0,

            speed=
                row["speed"] or 0.0,

            remaining_seconds=
                row["remaining_seconds"]
                if row["remaining_seconds"] is not None
                else -1,

            state=
                row["state"] or "waiting",

            paused=
                bool(row["paused"]),

            finished=
                bool(row["finished"]),

            successful=
                bool(row["successful"]),

            canceled=
                bool(row["canceled"]),

            interrupted=
                bool(row["interrupted"]),

            started_at=
                self._string_to_datetime(
                    row["started_at"]
                ),

            finished_at=
                self._string_to_datetime(
                    row["finished_at"]
                ),

            created_at=
                self._string_to_datetime(
                    row["created_at"]
                ),

            updated_at=
                self._string_to_datetime(
                    row["updated_at"]
                ),

            is_deleted=
                bool(row["is_deleted"]),

            # QWebEngine request only exists
            # while the application is running.
            _request=None,
        )

    # =================================================
    # Create
    # =================================================

    def add(
        self,
        item: DownloadItem,
    ) -> int:

        record = self.to_record(
            item
        )

        cursor = self.execute(

            f"""
            INSERT INTO {self.table}
            (
                uuid,
                filename,
                url,
                directory,
                mime_type,
                total_bytes,
                received_bytes,
                progress,
                speed,
                remaining_seconds,
                state,
                paused,
                finished,
                successful,
                canceled,
                interrupted,
                started_at,
                finished_at,
                created_at,
                updated_at,
                is_deleted
            )
            VALUES
            (
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,?
            )
            """,

            (

                record["uuid"],

                record["filename"],

                record["url"],

                record["directory"],

                record["mime_type"],

                record["total_bytes"],

                record["received_bytes"],

                record["progress"],

                record["speed"],

                record["remaining_seconds"],

                record["state"],

                record["paused"],

                record["finished"],

                record["successful"],

                record["canceled"],

                record["interrupted"],

                record["started_at"],

                record["finished_at"],

                record["created_at"],

                record["updated_at"],

                record["is_deleted"],

            ),
        )

        item.id = cursor.lastrowid

        return item.id

    # =================================================
    # Update
    # =================================================

    def update(
        self,
        item: DownloadItem,
    ) -> bool:

        record = self.to_record(
            item
        )

        self.execute(

            f"""
            UPDATE {self.table}
            SET

                uuid=?,

                filename=?,

                url=?,

                directory=?,

                mime_type=?,

                total_bytes=?,

                received_bytes=?,

                progress=?,

                speed=?,

                remaining_seconds=?,

                state=?,

                paused=?,

                finished=?,

                successful=?,

                canceled=?,

                interrupted=?,

                started_at=?,

                finished_at=?,

                updated_at=?,

                is_deleted=?

            WHERE id=?
            """,

            (

                record["uuid"],

                record["filename"],

                record["url"],

                record["directory"],

                record["mime_type"],

                record["total_bytes"],

                record["received_bytes"],

                record["progress"],

                record["speed"],

                record["remaining_seconds"],

                record["state"],

                record["paused"],

                record["finished"],

                record["successful"],

                record["canceled"],

                record["interrupted"],

                record["started_at"],

                record["finished_at"],

                record["updated_at"],

                record["is_deleted"],

                item.id,

            ),
        )

        return True

    # =================================================
    # Progress
    # =================================================

    def update_progress(
        self,
        item: DownloadItem,
    ) -> None:

        self.execute(

            f"""
            UPDATE {self.table}
            SET

                received_bytes=?,

                total_bytes=?,

                progress=?,

                speed=?,

                remaining_seconds=?,

                state=?,

                updated_at=?

            WHERE id=?
            """,

            (

                item.received_bytes,

                item.total_bytes,

                item.progress,

                item.speed,

                item.remaining_seconds,

                item.state,

                self._datetime_to_string(
                    item.updated_at
                ),

                item.id,

            ),
        )

    # =================================================
    # Find
    # =================================================

    def find_by_uuid(
        self,
        uuid: str,
    ) -> DownloadItem | None:

        row = self.execute(

            f"""
            SELECT *
            FROM {self.table}

            WHERE uuid=?
            AND is_deleted=0

            LIMIT 1
            """,

            (uuid,),

        ).fetchone()

        return self.from_record(
            row
        )

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
            AND is_deleted=0

            ORDER BY created_at DESC

            LIMIT 1
            """,

            (url,),

        ).fetchone()

        return self.from_record(
            row
        )

    # =================================================
    # Lists
    # =================================================

    def all_downloads(
        self,
    ) -> list[DownloadItem]:

        rows = self.execute(

            f"""
            SELECT *
            FROM {self.table}

            WHERE is_deleted=0

            ORDER BY created_at DESC
            """

        ).fetchall()

        return [

            self.from_record(row)

            for row in rows

        ]

    # -------------------------------------------------

    def active_downloads(
        self,
    ) -> list[DownloadItem]:

        rows = self.execute(

            f"""
            SELECT *
            FROM {self.table}

            WHERE is_deleted=0

            AND state IN
            (
                'waiting',
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

            WHERE is_deleted=0

            AND state='finished'

            ORDER BY updated_at DESC
            """

        ).fetchall()

        return [

            self.from_record(row)

            for row in rows

        ]

    # -------------------------------------------------

    def canceled_downloads(
        self,
    ) -> list[DownloadItem]:

        rows = self.execute(

            f"""
            SELECT *
            FROM {self.table}

            WHERE is_deleted=0

            AND state='canceled'

            ORDER BY updated_at DESC
            """

        ).fetchall()

        return [

            self.from_record(row)

            for row in rows

        ]

    # -------------------------------------------------

    def interrupted_downloads(
        self,
    ) -> list[DownloadItem]:

        rows = self.execute(

            f"""
            SELECT *
            FROM {self.table}

            WHERE is_deleted=0

            AND state='interrupted'

            ORDER BY updated_at DESC
            """

        ).fetchall()

        return [

            self.from_record(row)

            for row in rows

        ]

    # =================================================
    # Delete
    # =================================================

    def delete(
        self,
        item_id: int,
    ) -> bool:

        self.execute(

            f"""
            UPDATE {self.table}

            SET

                is_deleted=1,

                updated_at=?

            WHERE id=?
            """,

            (

                self._datetime_to_string(
                    datetime.now()
                ),

                item_id,

            ),
        )

        return True

    # =================================================
    # Clear
    # =================================================

    def clear_completed(
        self,
    ) -> None:

        self.execute(

            f"""
            UPDATE {self.table}

            SET

                is_deleted=1,

                updated_at=?

            WHERE state='finished'

            AND is_deleted=0
            """,

            (
                self._datetime_to_string(
                    datetime.now()
                ),
            ),
        )

    # -------------------------------------------------

    def clear_canceled(
        self,
    ) -> None:

        self.execute(

            f"""
            UPDATE {self.table}

            SET

                is_deleted=1,

                updated_at=?

            WHERE state='canceled'

            AND is_deleted=0
            """,

            (
                self._datetime_to_string(
                    datetime.now()
                ),
            ),
        )

    # -------------------------------------------------

    def clear_interrupted(
        self,
    ) -> None:

        self.execute(

            f"""
            UPDATE {self.table}

            SET

                is_deleted=1,

                updated_at=?

            WHERE state='interrupted'

            AND is_deleted=0
            """,

            (
                self._datetime_to_string(
                    datetime.now()
                ),
            ),
        )

    # =================================================
    # Statistics
    # =================================================

    def count_downloads(
        self,
    ) -> int:

        row = self.execute(

            f"""
            SELECT COUNT(*)
            FROM {self.table}

            WHERE is_deleted=0
            """

        ).fetchone()

        return row[0]

    # -------------------------------------------------

    def total_download_size(
        self,
    ) -> int:

        row = self.execute(

            f"""
            SELECT COALESCE(
                SUM(total_bytes),
                0
            )

            FROM {self.table}

            WHERE is_deleted=0

            AND state='finished'
            """

        ).fetchone()

        return row[0] or 0

    # =================================================
    # Helpers
    # =================================================

    @staticmethod
    def _datetime_to_string(
        value: datetime | None,
    ) -> str | None:

        if value is None:

            return None

        return value.isoformat()

    # -------------------------------------------------

    @staticmethod
    def _string_to_datetime(
        value: str | None,
    ) -> datetime:

        if not value:

            return datetime.now()

        try:

            return datetime.fromisoformat(
                value
            )

        except (
            TypeError,
            ValueError,
        ):

            return datetime.now()