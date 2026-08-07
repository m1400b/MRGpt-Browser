"""
MRGpt Browser

Browser Compatibility
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWebEngineCore import QWebEngineProfile

from core.browser.browser_info import BrowserInfo


class BrowserCompatibility:
    """
    Configure QWebEngineProfile
    for maximum browser compatibility.

    تمام تنظیمات مربوط به WebEngine
    فقط در این کلاس انجام می‌شود.
    """

    # -------------------------------------------------

    @classmethod
    def configure(
        cls,
        profile: QWebEngineProfile,
    ) -> None:

        info = BrowserInfo()

        cls._configure_user_agent(
            profile,
            info,
        )

        cls._configure_language(
            profile,
            info,
        )

        cls._configure_storage(
            profile,
        )

        cls._configure_cache(
            profile,
        )

        cls._configure_cookies(
            profile,
        )

    # -------------------------------------------------
    # User Agent
    # -------------------------------------------------

    @staticmethod
    def _configure_user_agent(
        profile: QWebEngineProfile,
        info: BrowserInfo,
    ) -> None:

        profile.setHttpUserAgent(
            info.user_agent
        )

    # -------------------------------------------------
    # Language
    # -------------------------------------------------

    @staticmethod
    def _configure_language(
        profile: QWebEngineProfile,
        info: BrowserInfo,
    ) -> None:

        profile.setHttpAcceptLanguage(
            info.accept_language
        )

    # -------------------------------------------------
    # Storage
    # -------------------------------------------------

    @staticmethod
    def _configure_storage(
        profile: QWebEngineProfile,
    ) -> None:

        base = (
            Path.home()
            / "AppData"
            / "Local"
            / "MRGpt"
        )

        storage = base / "storage"

        storage.mkdir(
            parents=True,
            exist_ok=True,
        )

        profile.setPersistentStoragePath(
            str(storage)
        )

    # -------------------------------------------------
    # Cache
    # -------------------------------------------------

    @staticmethod
    def _configure_cache(
        profile: QWebEngineProfile,
    ) -> None:

        base = (
            Path.home()
            / "AppData"
            / "Local"
            / "MRGpt"
        )

        cache = base / "cache"

        cache.mkdir(
            parents=True,
            exist_ok=True,
        )

        profile.setCachePath(
            str(cache)
        )

        profile.setHttpCacheType(
            QWebEngineProfile.DiskHttpCache
        )

    # -------------------------------------------------
    # Cookies
    # -------------------------------------------------

    @staticmethod
    def _configure_cookies(
        profile: QWebEngineProfile,
    ) -> None:

        profile.setPersistentCookiesPolicy(
            QWebEngineProfile.AllowPersistentCookies
        )