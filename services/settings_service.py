"""
MRGpt Browser

Settings Service
"""

from __future__ import annotations

from typing import Any

from core.settings.settings import Settings
from core.settings.settings_keys import SettingsKeys


class SettingsService:
    """
    Application settings service.

    این کلاس تنها نقطه دسترسی سایر بخش‌های
    برنامه به تنظیمات است.
    """

    # -------------------------------------------------

    def __init__(self) -> None:

        self._settings = Settings()

    # =================================================
    # Generic API
    # =================================================

    def value(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

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

        self._settings.set_value(
            key,
            value,
        )

    # -------------------------------------------------

    def restore_defaults(self) -> None:

        self._settings.restore_defaults()

    # -------------------------------------------------

    def sync(self) -> None:

        self._settings.sync()

    # =================================================
    # General
    # =================================================

    @property
    def language(self) -> str:

        return self.value(
            SettingsKeys.LANGUAGE
        )

    @language.setter
    def language(
        self,
        value: str,
    ) -> None:

        self.set_value(
            SettingsKeys.LANGUAGE,
            value,
        )

    # -------------------------------------------------

    @property
    def theme(self) -> str:

        return self.value(
            SettingsKeys.THEME
        )

    @theme.setter
    def theme(
        self,
        value: str,
    ) -> None:

        self.set_value(
            SettingsKeys.THEME,
            value,
        )

    # -------------------------------------------------

    @property
    def home_page(self) -> str:

        return self.value(
            SettingsKeys.HOME_PAGE
        )

    @home_page.setter
    def home_page(
        self,
        value: str,
    ) -> None:

        self.set_value(
            SettingsKeys.HOME_PAGE,
            value,
        )

    # =================================================
    # Startup
    # =================================================

    @property
    def startup_mode(self) -> str:

        return self.value(
            SettingsKeys.STARTUP_MODE
        )

    @startup_mode.setter
    def startup_mode(
        self,
        value: str,
    ) -> None:

        self.set_value(
            SettingsKeys.STARTUP_MODE,
            value,
        )

    # -------------------------------------------------

    @property
    def restore_session(self) -> bool:

        return bool(

            self.value(

                SettingsKeys.RESTORE_SESSION

            )

        )

    @restore_session.setter
    def restore_session(
        self,
        value: bool,
    ) -> None:

        self.set_value(

            SettingsKeys.RESTORE_SESSION,

            value,

        )

    # -------------------------------------------------

    @property
    def check_updates(self) -> bool:

        return bool(

            self.value(

                SettingsKeys.CHECK_UPDATES

            )

        )

    @check_updates.setter
    def check_updates(
        self,
        value: bool,
    ) -> None:

        self.set_value(

            SettingsKeys.CHECK_UPDATES,

            value,

        )
    
    # =================================================
    # Downloads
    # =================================================

    @property
    def download_path(self) -> str:

        return self.value(
            SettingsKeys.DOWNLOAD_PATH
        )

    @download_path.setter
    def download_path(
        self,
        value: str,
    ) -> None:

        self.set_value(
            SettingsKeys.DOWNLOAD_PATH,
            value,
        )

    # =================================================
    # Privacy
    # =================================================

    @property
    def cookies_enabled(self) -> bool:

        return bool(

            self.value(

                SettingsKeys.ACCEPT_COOKIES

            )

        )

    @cookies_enabled.setter
    def cookies_enabled(
        self,
        value: bool,
    ) -> None:

        self.set_value(

            SettingsKeys.ACCEPT_COOKIES,

            value,

        )

    # =================================================
    # Appearance
    # =================================================

    @property
    def zoom_factor(self) -> float:

        return float(

            self.value(

                SettingsKeys.ZOOM_FACTOR

            )

        )

    @zoom_factor.setter
    def zoom_factor(
        self,
        value: float,
    ) -> None:

        self.set_value(

            SettingsKeys.ZOOM_FACTOR,

            value,

        )

    # =================================================

    @property
    def settings(self) -> Settings:

        """
        دسترسی مستقیم در صورت نیاز.
        """

        return self._settings