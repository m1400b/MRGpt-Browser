"""
MRGpt Browser

Connection Service
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from PySide6.QtCore import QObject, Signal

from core.config.config_manager import config


class NetworkService(QObject):
    """
    مدیریت Connection Profile ها

    این کلاس فعلاً فقط Profile ها را مدیریت می‌کند.
    در Release های بعدی موتور sing-box به آن متصل خواهد شد.
    """

    profiles_changed = Signal()

    active_profile_changed = Signal(str)

    # ---------------------------------------------------------

    def __init__(self, parent=None):

        super().__init__(parent)

        self._connections_dir = (
            Path(__file__).resolve().parents[1]
            / "connections"
        )

        self._connections_dir.mkdir(
            exist_ok=True
        )

        self._profiles: Dict[str, Path] = {}

        self._active: Optional[str] = None

        self.reload()

    # ---------------------------------------------------------

    def reload(self) -> None:
        """
        Scan connections directory
        """

        self._profiles.clear()

        extensions = {

            ".json",
            ".yaml",
            ".yml",
            ".conf",
            ".txt"

        }

        for file in self._connections_dir.iterdir():

            if not file.is_file():
                continue

            if file.suffix.lower() not in extensions:
                continue

            self._profiles[file.stem] = file

        active = config.get(
            "network",
            "active_profile",
            ""
        )

        if active in self._profiles:

            self._active = active

        else:

            self._active = None

        self.profiles_changed.emit()

    # ---------------------------------------------------------

    def profiles(self) -> Dict[str, Path]:

        return self._profiles.copy()

    # ---------------------------------------------------------

    def names(self) -> list[str]:

        return sorted(self._profiles.keys())

    # ---------------------------------------------------------

    def exists(
        self,
        name: str
    ) -> bool:

        return name in self._profiles

    # ---------------------------------------------------------

    def path(
        self,
        name: str
    ) -> Optional[Path]:

        return self._profiles.get(name)

    # ---------------------------------------------------------

    def active(self) -> Optional[str]:

        return self._active

    # ---------------------------------------------------------

    def active_path(self) -> Optional[Path]:

        if self._active is None:

            return None

        return self._profiles.get(
            self._active
        )

    # ---------------------------------------------------------

    def set_active(
        self,
        name: str
    ) -> None:

        if name not in self._profiles:

            raise KeyError(
                f'Connection "{name}" not found.'
            )

        self._active = name

        config.set(
            "network",
            "active_profile",
            name
        )

        config.save()

        self.active_profile_changed.emit(
            name
        )

    # ---------------------------------------------------------

    def clear_active(self):

        self._active = None

        config.set(
            "network",
            "active_profile",
            ""
        )

        config.save()

    # ---------------------------------------------------------

    def count(self) -> int:

        return len(self._profiles)