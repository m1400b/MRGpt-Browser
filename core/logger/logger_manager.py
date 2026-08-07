"""
MRGpt Browser

Logger Manager
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class LoggerManager:
    """
    Global Logger Manager
    """

    _instance = None

    # ---------------------------------------------------------

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance._initialized = False

        return cls._instance

    # ---------------------------------------------------------

    def __init__(self):

        if self._initialized:
            return

        self._initialized = True

        self.log_dir = Path("logs")

        self.log_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self._loggers = {}

    # ---------------------------------------------------------

    def get_logger(
        self,
        name: str
    ) -> logging.Logger:

        if name in self._loggers:

            return self._loggers[name]

        logger = logging.getLogger(name)

        logger.setLevel(logging.DEBUG)

        logger.propagate = False

        if not logger.handlers:

            file_handler = RotatingFileHandler(

                self.log_dir / f"{name}.log",

                maxBytes=5 * 1024 * 1024,

                backupCount=5,

                encoding="utf-8"

            )

            formatter = logging.Formatter(

                "[%(asctime)s] "

                "[%(levelname)s] "

                "[%(name)s] "

                "%(message)s",

                "%Y-%m-%d %H:%M:%S"

            )

            file_handler.setFormatter(
                formatter
            )

            logger.addHandler(
                file_handler
            )

            console_handler = logging.StreamHandler()

            console_handler.setFormatter(
                formatter
            )

            logger.addHandler(
                console_handler
            )

        self._loggers[name] = logger

        return logger

    # ---------------------------------------------------------

    def browser(self):

        return self.get_logger(
            "browser"
        )

    # ---------------------------------------------------------

    def network(self):

        return self.get_logger(
            "network"
        )

    # ---------------------------------------------------------

    def javascript(self):

        return self.get_logger(
            "javascript"
        )

    # ---------------------------------------------------------

    def ssl(self):

        return self.get_logger(
            "ssl"
        )

    # ---------------------------------------------------------

    def vpn(self):

        return self.get_logger(
            "vpn"
        )

    # ---------------------------------------------------------

    def download(self):

        return self.get_logger(
            "download"
        )

    # ---------------------------------------------------------

    def history(self):

        return self.get_logger(
            "history"
        )

    # ---------------------------------------------------------

    def bookmark(self):

        return self.get_logger(
            "bookmark"
        )

    # ---------------------------------------------------------

    def performance(self):

        return self.get_logger(
            "performance"
        )

    # ---------------------------------------------------------

    def ai(self):

        return self.get_logger(
            "ai"
        )


logger = LoggerManager()