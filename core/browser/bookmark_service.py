"""
MRGpt Browser

Bookmark Service

مدیریت صفحات نشان شده
"""


from __future__ import annotations


import sqlite3

from pathlib import Path

from datetime import datetime



class BookmarkService:


    def __init__(
        self,
        db_path="database/browser_bookmarks.db"
    ):


        self.db_path = Path(
            db_path
        )


        self.db_path.parent.mkdir(
            exist_ok=True
        )


        self._create_database()



    # ---------------------------------

    def _connect(self):

        return sqlite3.connect(
            self.db_path
        )



    # ---------------------------------

    def _create_database(self):


        with self._connect() as conn:


            cursor = conn.cursor()


            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS bookmarks
                (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,


                    title TEXT,


                    url TEXT UNIQUE,


                    icon TEXT,


                    created_at TEXT

                )
                """
            )


            conn.commit()



    # ---------------------------------

    def add(
        self,
        url,
        title="",
        icon=""
    ):

        """
        اضافه کردن Bookmark
        """


        with self._connect() as conn:


            cursor = conn.cursor()


            try:

                cursor.execute(
                    """
                    INSERT INTO bookmarks
                    (
                        title,
                        url,
                        icon,
                        created_at
                    )

                    VALUES
                    (
                        ?,
                        ?,
                        ?,
                        ?
                    )

                    """,
                    (
                        title,
                        url,
                        icon,
                        datetime.now().isoformat()
                    )
                )


                conn.commit()


                return True


            except sqlite3.IntegrityError:


                return False



    # ---------------------------------

    def remove(
        self,
        url
    ):


        with self._connect() as conn:


            cursor = conn.cursor()


            cursor.execute(
                """
                DELETE FROM bookmarks

                WHERE url = ?

                """,
                (
                    url,
                )
            )


            conn.commit()



    # ---------------------------------

    def exists(
        self,
        url
    ):


        with self._connect() as conn:


            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT id

                FROM bookmarks

                WHERE url = ?

                """,
                (
                    url,
                )
            )


            return (
                cursor.fetchone()
                is not None
            )



    # ---------------------------------

    def get_all(self):


        with self._connect() as conn:


            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT

                    id,
                    title,
                    url,
                    icon,
                    created_at


                FROM bookmarks


                ORDER BY id DESC

                """
            )


            return cursor.fetchall()



    # ---------------------------------

    def search(
        self,
        text
    ):


        with self._connect() as conn:


            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT

                    id,
                    title,
                    url


                FROM bookmarks


                WHERE

                    title LIKE ?

                    OR

                    url LIKE ?


                ORDER BY id DESC

                """,
                (
                    f"%{text}%",
                    f"%{text}%"
                )
            )


            return cursor.fetchall()



    # ---------------------------------

    def clear(self):


        with self._connect() as conn:


            cursor = conn.cursor()


            cursor.execute(
                """
                DELETE FROM bookmarks
                """
            )


            conn.commit()