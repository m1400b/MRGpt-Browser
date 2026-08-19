"""
MRGpt Browser

Service Names
"""

from __future__ import annotations

from typing import Final


class ServiceNames:
    """
    Registered service identifiers.
    """

    # -------------------------------------------------
    # Core
    # -------------------------------------------------

    SETTINGS: Final[str] = "settings"

    PROFILE: Final[str] = "profile"

    BROWSER: Final[str] = "browser"
    
    APPEARANCE: Final[str] = "appearance"
    
    DATABASE: Final[str] = "database"

    # -------------------------------------------------
    # Browser
    # -------------------------------------------------

    COOKIES: Final[str] = "cookies"

    DOWNLOADS: Final[str] = "downloads"

    HISTORY: Final[str] = "history"

    BOOKMARKS: Final[str] = "bookmarks"

    PASSWORDS: Final[str] = "passwords"

    PERMISSIONS: Final[str] = "permissions"

    # -------------------------------------------------
    # Network
    # -------------------------------------------------

    VPN: Final[str] = "vpn"

    PROXY: Final[str] = "proxy"

    NETWORK: Final[str] = "network"

    # -------------------------------------------------
    # Engine
    # -------------------------------------------------

    MEDIA: Final[str] = "media"

    DOWNLOAD_ENGINE: Final[str] = "download_engine"

    SEARCH: Final[str] = "search"

    # -------------------------------------------------
    # AI
    # -------------------------------------------------

    AI: Final[str] = "ai"

    PROMPT: Final[str] = "prompt"

    # -------------------------------------------------
    # Application
    # -------------------------------------------------

    LOGGER: Final[str] = "logger"

    CONFIG: Final[str] = "config"

    EVENT_BUS: Final[str] = "event_bus"