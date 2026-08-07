"""
MRGpt Browser

Default Settings
"""

from __future__ import annotations

from pathlib import Path

from core.settings.settings_keys import SettingsKeys


class SettingsDefaults:
    """
    Default application settings.

    این کلاس فقط مقادیر پیش‌فرض تنظیمات را نگهداری می‌کند.
    """

    DEFAULTS = {

        # -------------------------------------------------
        # General
        # -------------------------------------------------

        SettingsKeys.LANGUAGE:
            "fa-IR",

        SettingsKeys.THEME:
            "System",

        SettingsKeys.STARTUP_MODE:
            "home",

        SettingsKeys.HOME_PAGE:
            "https://www.google.com",

        SettingsKeys.RESTORE_SESSION:
            True,

        SettingsKeys.CHECK_UPDATES:
            True,

        # -------------------------------------------------
        # Appearance
        # -------------------------------------------------

        SettingsKeys.ZOOM_FACTOR:
            1.0,

        SettingsKeys.UI_SCALE:
            1.0,

        SettingsKeys.SHOW_STATUS_BAR:
            True,

        SettingsKeys.SHOW_BOOKMARK_BAR:
            True,

        # -------------------------------------------------
        # Downloads
        # -------------------------------------------------

        SettingsKeys.DOWNLOAD_PATH:
            str(Path.home() / "Downloads"),

        SettingsKeys.ASK_DOWNLOAD_LOCATION:
            True,

        SettingsKeys.OPEN_AFTER_DOWNLOAD:
            False,

        # -------------------------------------------------
        # Privacy
        # -------------------------------------------------

        SettingsKeys.ACCEPT_COOKIES:
            True,

        SettingsKeys.SAVE_HISTORY:
            True,

        SettingsKeys.SAVE_PASSWORDS:
            False,

        SettingsKeys.SEND_DO_NOT_TRACK:
            False,

        SettingsKeys.CLEAR_CACHE_ON_EXIT:
            False,

        SettingsKeys.CLEAR_COOKIES_ON_EXIT:
            False,

        # -------------------------------------------------
        # Search
        # -------------------------------------------------

        SettingsKeys.SEARCH_ENGINE:
            "google",

        SettingsKeys.SEARCH_URL:
            "",

        # -------------------------------------------------
        # Tabs
        # -------------------------------------------------

        SettingsKeys.OPEN_LINKS_IN_BACKGROUND:
            False,

        SettingsKeys.CONFIRM_CLOSE_MULTIPLE:
            True,

        SettingsKeys.TAB_POSITION:
            "top",

        # -------------------------------------------------
        # Network
        # -------------------------------------------------

        SettingsKeys.PROXY_ENABLED:
            False,

        SettingsKeys.PROXY_HOST:
            "",

        SettingsKeys.PROXY_PORT:
            0,

        SettingsKeys.VPN_ENABLED:
            False,

        # -------------------------------------------------
        # AI
        # -------------------------------------------------

        SettingsKeys.AI_PROVIDER:
            "ollama",

        SettingsKeys.AI_MODEL:
            "",

        SettingsKeys.AI_ENDPOINT:
            "http://127.0.0.1:11434",

        SettingsKeys.AI_API_KEY:
            "",

        # -------------------------------------------------
        # Security
        # -------------------------------------------------

        SettingsKeys.ENABLE_JAVASCRIPT:
            True,

        SettingsKeys.ENABLE_POPUPS:
            False,

        SettingsKeys.ENABLE_PDF_VIEWER:
            True,

        SettingsKeys.ENABLE_WEBRTC:
            True,

        # -------------------------------------------------
        # Advanced
        # -------------------------------------------------

        SettingsKeys.USER_AGENT:
            "",

        SettingsKeys.CACHE_SIZE:
            512,

        SettingsKeys.DEVELOPER_MODE:
            False,

        SettingsKeys.LOG_LEVEL:
            "INFO",
    }

    # -------------------------------------------------

    @classmethod
    def value(cls, key: str):

        """
        Return default value for a key.
        """

        return cls.DEFAULTS.get(key)

    # -------------------------------------------------

    @classmethod
    def all(cls) -> dict:

        """
        Return a copy of all default settings.
        """

        return dict(cls.DEFAULTS)