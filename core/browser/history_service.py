"""
MRGpt Browser

History Service

مدیریت تاریخچه مرورگر
"""


from __future__ import annotations


import sqlite3

from pathlib import Path

from datetime import datetime



class HistoryService:


    def __init__(
        self,
        db_path="database/browser_history.db"
    ):


        self.db_path = Path(
            db_path
        )


        self.db_path.parent.mkdir(
            exist_ok=True
        )


        self._create_database()



    # ----------------------------------

    def _connect(self):

        return sqlite3.connect(
            self.db_path
        )



    # ----------------------------------

    def _create_database(self):


        with self._connect() as conn:


            cursor = conn.cursor()


            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS history
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    url TEXT NOT NULL,

                    title TEXT,

                    visit_time TEXT
                )
                """
            )


            conn.commit()



    # ----------------------------------

    def add_visit(
        self,
        url,
        title=""
    ):


        with self._connect() as conn:


            cursor = conn.cursor()


            cursor.execute(
                """
                INSERT INTO history
                (
                    url,
                    title,
                    visit_time
                )

                VALUES
                (
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    url,
                    title,
                    datetime.now().isoformat()
                )
            )


            conn.commit()



    # ----------------------------------

    def get_all(
        self,
        limit=200
    ):


        with self._connect() as conn:


            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT
                    url,
                    title,
                    visit_time

                FROM history

                ORDER BY id DESC

                LIMIT ?
                """,
                (
                    limit,
                )
            )


            return cursor.fetchall()



    # ----------------------------------

    def search(
        self,
        text
    ):


        with self._connect() as conn:


            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT
                    url,
                    title,
                    visit_time

                FROM history

                WHERE
                    url LIKE ?
                    OR
                    title LIKE ?

                ORDER BY id DESC

                """,
                (
                    f"%{text}%",
                    f"%{text}%"
                )
            )


            return cursor.fetchall()



    # ----------------------------------

    def clear(self):


        with self._connect() as conn:


            cursor = conn.cursor()


            cursor.execute(
                """
                DELETE FROM history
                """
            )


            conn.commit()