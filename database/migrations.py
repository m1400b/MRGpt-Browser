"""
MRGpt Browser

Database Migrations
"""

from __future__ import annotations

import sqlite3


class MigrationManager:
    """
    Create application database schema.
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
        Create all application tables.
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

    # =================================================
    # Downloads
    # =================================================
    
    def _create_download_table(self):
    
        self.connection.execute(
        
            """
            CREATE TABLE IF NOT EXISTS downloads(
    
                id INTEGER PRIMARY KEY AUTOINCREMENT,
    
                uuid TEXT NOT NULL UNIQUE,
    
                filename TEXT,
    
                url TEXT,
    
                directory TEXT,
    
                mime_type TEXT,
    
                total_bytes INTEGER DEFAULT 0,
    
                received_bytes INTEGER DEFAULT 0,
    
                progress REAL DEFAULT 0.0,
    
                speed REAL DEFAULT 0.0,
    
                remaining_seconds INTEGER DEFAULT -1,
    
                state TEXT DEFAULT 'waiting',
    
                paused INTEGER DEFAULT 0,
    
                finished INTEGER DEFAULT 0,
    
                successful INTEGER DEFAULT 0,
    
                canceled INTEGER DEFAULT 0,
    
                interrupted INTEGER DEFAULT 0,
    
                started_at TEXT,
    
                finished_at TEXT,
    
                created_at TEXT,
    
                updated_at TEXT,
    
                is_deleted INTEGER DEFAULT 0
    
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

