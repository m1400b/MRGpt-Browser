"""
MRGpt Browser

Settings Keys
"""

from __future__ import annotations


class SettingsKeys:
    """
    Application settings keys.

    این کلاس فقط کلیدهای تنظیمات را نگهداری می‌کند.
    """

    # -------------------------------------------------
    # General
    # -------------------------------------------------

    LANGUAGE = "general/language"

    THEME = "general/theme"

    STARTUP_MODE = "general/startup_mode"

    HOME_PAGE = "general/home_page"

    RESTORE_SESSION = "general/restore_session"

    CHECK_UPDATES = "general/check_updates"

    # -------------------------------------------------
    # Appearance
    # -------------------------------------------------

    ZOOM_FACTOR = "appearance/zoom_factor"

    UI_SCALE = "appearance/ui_scale"

    SHOW_STATUS_BAR = "appearance/show_status_bar"

    SHOW_BOOKMARK_BAR = "appearance/show_bookmark_bar"

    # -------------------------------------------------
    # Downloads
    # -------------------------------------------------

    DOWNLOAD_PATH = "downloads/path"

    ASK_DOWNLOAD_LOCATION = "downloads/ask_location"

    OPEN_AFTER_DOWNLOAD = "downloads/open_after_download"

    # -------------------------------------------------
    # Privacy
    # -------------------------------------------------

    ACCEPT_COOKIES = "privacy/accept_cookies"

    SAVE_HISTORY = "privacy/save_history"

    SAVE_PASSWORDS = "privacy/save_passwords"

    SEND_DO_NOT_TRACK = "privacy/do_not_track"

    CLEAR_CACHE_ON_EXIT = "privacy/clear_cache_on_exit"

    CLEAR_COOKIES_ON_EXIT = "privacy/clear_cookies_on_exit"

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    SEARCH_ENGINE = "search/default_engine"

    SEARCH_URL = "search/custom_url"

    # -------------------------------------------------
    # Tabs
    # -------------------------------------------------

    OPEN_LINKS_IN_BACKGROUND = "tabs/open_in_background"

    CONFIRM_CLOSE_MULTIPLE = "tabs/confirm_close_multiple"

    TAB_POSITION = "tabs/position"

    # -------------------------------------------------
    # Network
    # -------------------------------------------------

    PROXY_ENABLED = "network/proxy_enabled"

    PROXY_HOST = "network/proxy_host"

    PROXY_PORT = "network/proxy_port"

    VPN_ENABLED = "network/vpn_enabled"

    # -------------------------------------------------
    # AI
    # -------------------------------------------------

    AI_PROVIDER = "ai/provider"

    AI_MODEL = "ai/model"

    AI_ENDPOINT = "ai/endpoint"

    AI_API_KEY = "ai/api_key"

    # -------------------------------------------------
    # Security
    # -------------------------------------------------

    ENABLE_JAVASCRIPT = "security/javascript"

    ENABLE_POPUPS = "security/popups"

    ENABLE_PDF_VIEWER = "security/pdf_viewer"

    ENABLE_WEBRTC = "security/webrtc"

    # -------------------------------------------------
    # Advanced
    # -------------------------------------------------

    USER_AGENT = "advanced/user_agent"

    CACHE_SIZE = "advanced/cache_size"

    DEVELOPER_MODE = "advanced/developer_mode"

    LOG_LEVEL = "advanced/log_level"