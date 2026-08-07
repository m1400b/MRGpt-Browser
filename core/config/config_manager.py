"""
MRGpt Browser

Configuration Manager
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ConfigManager:

    def __init__(self):

        self._config_dir = Path("config")

        self._config_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self._config_file = (
            self._config_dir / "settings.json"
        )

        self._data: dict[str, Any] = {}

        self.load()

    # ---------------------------------------------------------

    def load(self) -> None:

        if not self._config_file.exists():

            self._create_default()

            return

        try:

            with open(
                self._config_file,
                "r",
                encoding="utf-8"
            ) as f:

                self._data = json.load(f)

        except Exception:

            self._create_default()

    # ---------------------------------------------------------

    def save(self) -> None:

        with open(
            self._config_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self._data,
                f,
                indent=4,
                ensure_ascii=False
            )

    # ---------------------------------------------------------

    def _create_default(self):

        self._data = {

            "application": {

                "name": "MRGpt",

                "version": "0.1.0"

            },

            "window": {

                "width": 1500,

                "height": 900,

                "maximized": False

            },

            "browser": {

                "home_page": "https://www.google.com",

                "search_engine":
                    "https://www.google.com/search?q={}",

                "default_zoom": 1.0

            },

            "network": {

                "active_profile": "",

                "auto_connect": False

            },

            "download": {

                "directory": "downloads"

            },

            "ui": {

                "theme": "light",

                "language": "fa"

            }

        }

        self.save()

    # ---------------------------------------------------------

    def get(

        self,

        section: str,

        key: str,

        default=None

    ):

        return self._data.get(

            section,

            {}

        ).get(

            key,

            default

        )

    # ---------------------------------------------------------

    def set(

        self,

        section: str,

        key: str,

        value

    ):

        if section not in self._data:

            self._data[section] = {}

        self._data[section][key] = value

    # ---------------------------------------------------------

    def remove(

        self,

        section: str,

        key: str

    ):

        if section in self._data:

            self._data[section].pop(

                key,

                None

            )

    # ---------------------------------------------------------

    def section(

        self,

        name: str

    ):

        return self._data.setdefault(

            name,

            {}

        )

    # ---------------------------------------------------------

    def contains(

        self,

        section: str,

        key: str

    ) -> bool:

        return (

            section in self._data

            and

            key in self._data[section]

        )

    # ---------------------------------------------------------

    @property
    def data(self):

        return self._data

    # ---------------------------------------------------------

    @property
    def file(self):

        return self._config_file


config = ConfigManager()