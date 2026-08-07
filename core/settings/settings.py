"""
MRGpt Browser

Application Settings
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QSettings

from core.settings.settings_defaults import SettingsDefaults


class Settings:
    """
    Central application settings manager.

    تمام تنظیمات برنامه از طریق این کلاس
    خوانده و ذخیره می‌شوند.
    """

    ORGANIZATION = "MRGpt"

    APPLICATION = "Browser"

    # -------------------------------------------------

    def __init__(self) -> None:

        self._settings = QSettings(

            self.ORGANIZATION,

            self.APPLICATION,

        )

    # -------------------------------------------------

    def value(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Read setting value.
        """

        if default is None:

            default = SettingsDefaults.value(
                key
            )

        return self._settings.value(
            key,
            default,
        )

    # -------------------------------------------------

    def set_value(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Save setting value.
        """

        self._settings.setValue(
            key,
            value,
        )

    # -------------------------------------------------

    def contains(
        self,
        key: str,
    ) -> bool:
        """
        Check setting exists.
        """

        return self._settings.contains(
            key
        )

    # -------------------------------------------------

    def remove(
        self,
        key: str,
    ) -> None:
        """
        Remove one setting.
        """

        self._settings.remove(
            key
        )

    # -------------------------------------------------

    def clear(self) -> None:
        """
        Remove all settings.
        """

        self._settings.clear()

    # -------------------------------------------------

    def sync(self) -> None:
        """
        Flush settings to disk.
        """

        self._settings.sync()

    # -------------------------------------------------

    def restore_defaults(self) -> None:
        """
        Restore all default settings.
        """

        self.clear()

        for key, value in SettingsDefaults.all().items():

            self.set_value(
                key,
                value,
            )

        self.sync()

    # -------------------------------------------------

    def all_keys(self) -> list[str]:
        """
        Return all stored keys.
        """

        return self._settings.allKeys()

    # -------------------------------------------------

    def file_name(self) -> str:
        """
        Return settings file path.
        """

        return self._settings.fileName()

    # -------------------------------------------------

    @property
    def qt_settings(self) -> QSettings:
        """
        Access underlying QSettings.
        """

        return self._settings