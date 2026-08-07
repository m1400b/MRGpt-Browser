"""
MRGpt Browser

Database Migrations
"""

from __future__ import annotations

import sqlite3


class MigrationManager:
    """
    Create and upgrade database schema.
    """

    # -------------------------------------------------

    def __init__(

        self,

        connection: sqlite3.Connection,

    ):

        self.connection = connection

    # -------------------------------------------------

    def migrate(self):

        """
        Run all migrations.
        """

        self._create_history_table()

        self._create_bookmark_table()

        self._create_download_table()

        self._create_settings_table()

        self._create_ai_session_table()

        self._create_ai_message_table()

        self._create_vpn_table()

        self.connection.commit()

    # =================================================
    # History
    # =================================================

    def _create_history_table(self):

        self.connection.execute(

            """
            CREATE TABLE IF NOT EXISTS history(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT,

                url TEXT NOT NULL,

                visit_time TEXT,

                visit_count INTEGER DEFAULT 1,

                favicon TEXT,

                created_at TEXT,

                updated_at TEXT

            )
            """

        )

    # =================================================
    # Bookmark
    # =================================================

    def _create_bookmark_table(self):

        self.connection.execute(

            """
            CREATE TABLE IF NOT EXISTS bookmarks(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT,

                url TEXT NOT NULL,

                folder TEXT,

                description TEXT,

                favorite INTEGER DEFAULT 0,

                created_at TEXT,

                updated_at TEXT

            )
            """

        )

    # =================================================
    # Downloads
    # =================================================

    def _create_download_table(self):

        self.connection.execute(

            """
            CREATE TABLE IF NOT EXISTS downloads(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                url TEXT,

                file_name TEXT,

                save_path TEXT,

                mime_type TEXT,

                total_bytes INTEGER,

                received_bytes INTEGER,

                state TEXT,

                created_at TEXT,

                updated_at TEXT

            )
            """

        )

    # =================================================
    # Settings
    # =================================================

    def _create_settings_table(self):

        self.connection.execute(

            """
            CREATE TABLE IF NOT EXISTS settings(

                key TEXT PRIMARY KEY,

                value TEXT

            )
            """

        )

    # =================================================
    # AI Sessions
    # =================================================

    def _create_ai_session_table(self):

        self.connection.execute(

            """
            CREATE TABLE IF NOT EXISTS ai_sessions(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT,

                provider TEXT,

                model TEXT,

                system_prompt TEXT,

                message_count INTEGER,

                prompt_tokens INTEGER,

                completion_tokens INTEGER,

                total_tokens INTEGER,

                created_at TEXT,

                updated_at TEXT

            )
            """

        )

    # =================================================
    # AI Messages
    # =================================================

    def _create_ai_message_table(self):

        self.connection.execute(

            """
            CREATE TABLE IF NOT EXISTS ai_messages(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                session_id INTEGER,

                role TEXT,

                content TEXT,

                reasoning TEXT,

                prompt_tokens INTEGER,

                completion_tokens INTEGER,

                total_tokens INTEGER,

                created_at TEXT,

                updated_at TEXT,

                FOREIGN KEY(session_id)

                REFERENCES ai_sessions(id)

                ON DELETE CASCADE

            )
            """

        )

    # =================================================
    # VPN
    # =================================================

    def _create_vpn_table(self):

        self.connection.execute(

            """
            CREATE TABLE IF NOT EXISTS vpn_configs(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT,

                protocol TEXT,

                server TEXT,

                port INTEGER,

                username TEXT,

                password TEXT,

                config_path TEXT,

                enabled INTEGER,

                favorite INTEGER,

                created_at TEXT,

                updated_at TEXT

            )
            """

        )