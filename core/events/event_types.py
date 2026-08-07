"""
MRGpt Browser

Event Types
"""

from __future__ import annotations

from enum import StrEnum


class EventType(StrEnum):

    # =================================================
    # Browser
    # =================================================

    BROWSER_STARTED = "browser.started"

    BROWSER_CLOSED = "browser.closed"

    PAGE_LOADING = "page.loading"

    PAGE_LOADED = "page.loaded"

    PAGE_TITLE_CHANGED = "page.title_changed"

    PAGE_ICON_CHANGED = "page.icon_changed"

    URL_CHANGED = "browser.url_changed"

    NEW_TAB = "browser.new_tab"

    TAB_CLOSED = "browser.tab_closed"

    TAB_CHANGED = "browser.tab_changed"

    DOWNLOAD_REQUESTED = "browser.download_requested"

    # =================================================
    # History
    # =================================================

    HISTORY_VISIT = "history.visit"

    HISTORY_ADDED = "history.added"

    HISTORY_UPDATED = "history.updated"

    HISTORY_REMOVED = "history.removed"

    HISTORY_CLEARED = "history.cleared"

    # =================================================
    # Bookmark
    # =================================================

    BOOKMARK_ADDED = "bookmark.added"

    BOOKMARK_UPDATED = "bookmark.updated"

    BOOKMARK_REMOVED = "bookmark.removed"

    BOOKMARK_MOVED = "bookmark.moved"

    BOOKMARK_FOLDER_CREATED = "bookmark.folder_created"

    BOOKMARK_FOLDER_REMOVED = "bookmark.folder_removed"

    # =================================================
    # Download
    # =================================================

    DOWNLOAD_STARTED = "download.started"

    DOWNLOAD_PROGRESS = "download.progress"

    DOWNLOAD_PAUSED = "download.paused"

    DOWNLOAD_RESUMED = "download.resumed"

    DOWNLOAD_FINISHED = "download.finished"

    DOWNLOAD_FAILED = "download.failed"

    DOWNLOAD_CANCELLED = "download.cancelled"

    # =================================================
    # AI
    # =================================================

    AI_REQUEST = "ai.request"

    AI_RESPONSE = "ai.response"

    AI_STREAM = "ai.stream"

    AI_FINISHED = "ai.finished"

    AI_ERROR = "ai.error"

    # =================================================
    # VPN
    # =================================================

    VPN_CONNECTING = "vpn.connecting"

    VPN_CONNECTED = "vpn.connected"

    VPN_DISCONNECTED = "vpn.disconnected"

    VPN_ERROR = "vpn.error"

    # =================================================
    # Settings
    # =================================================

    SETTINGS_CHANGED = "settings.changed"

    THEME_CHANGED = "theme.changed"

    LANGUAGE_CHANGED = "language.changed"

    # =================================================
    # Session
    # =================================================

    SESSION_CREATED = "session.created"

    SESSION_RESTORED = "session.restored"

    SESSION_SAVED = "session.saved"

    SESSION_CLOSED = "session.closed"

    # =================================================
    # Window
    # =================================================

    WINDOW_OPENED = "window.opened"

    WINDOW_CLOSED = "window.closed"

    WINDOW_MAXIMIZED = "window.maximized"

    WINDOW_MINIMIZED = "window.minimized"

    WINDOW_FULLSCREEN = "window.fullscreen"

    # =================================================
    # Extensions
    # =================================================

    EXTENSION_LOADED = "extension.loaded"

    EXTENSION_UNLOADED = "extension.unloaded"

    PLUGIN_LOADED = "plugin.loaded"

    PLUGIN_UNLOADED = "plugin.unloaded"

    # =================================================
    # Network
    # =================================================

    NETWORK_ONLINE = "network.online"

    NETWORK_OFFLINE = "network.offline"

    PROXY_CHANGED = "network.proxy_changed"

    # =================================================
    # Application
    # =================================================

    APPLICATION_STARTED = "application.started"

    APPLICATION_EXITING = "application.exiting"

    APPLICATION_ERROR = "application.error"

    APPLICATION_SHUTDOWN = "application.shutdown"