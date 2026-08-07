"""
MRGpt Browser

Browser Settings
"""

from __future__ import annotations

from dataclasses import dataclass, field

from models.settings_model import SettingsModel


@dataclass(slots=True)
class BrowserSettings(SettingsModel):
    """
    Browser Settings Model
    """

    # -------------------------------------------------
    # Startup
    # -------------------------------------------------

    homepage: str = "https://www.google.com"

    restore_session: bool = True

    start_maximized: bool = True

    # -------------------------------------------------
    # Appearance
    # -------------------------------------------------

    dark_mode: bool = False

    language: str = "fa-IR"

    zoom_factor: float = 1.0

    smooth_scroll: bool = True

    # -------------------------------------------------
    # Privacy
    # -------------------------------------------------

    javascript_enabled: bool = True

    cookies_enabled: bool = True

    local_storage_enabled: bool = False

    do_not_track: bool = True

    send_referrer: bool = False

    # -------------------------------------------------
    # Downloads
    # -------------------------------------------------

    ask_download_path: bool = True

    download_directory: str = ""

    overwrite_existing: bool = False

    # -------------------------------------------------
    # Tabs
    # -------------------------------------------------

    open_links_in_background: bool = False

    confirm_before_closing: bool = True

    show_tab_close_button: bool = True

    # -------------------------------------------------
    # Network
    # -------------------------------------------------

    dns_prefetch: bool = True

    use_system_proxy: bool = True

    enable_vpn: bool = False

    # -------------------------------------------------
    # Performance
    # -------------------------------------------------

    enable_gpu: bool = True

    enable_cache: bool = False

    max_cache_size_mb: int = 128

    lazy_load_tabs: bool = True

    # -------------------------------------------------
    # Developer
    # -------------------------------------------------

    developer_tools: bool = False

    verbose_logging: bool = False

    # -------------------------------------------------

    def reset(self):
        """
        Restore default browser settings.
        """

        self.homepage = "https://www.google.com"

        self.restore_session = True

        self.start_maximized = True

        self.dark_mode = False

        self.language = "fa-IR"

        self.zoom_factor = 1.0

        self.smooth_scroll = True

        self.javascript_enabled = True

        self.cookies_enabled = True

        self.local_storage_enabled = False

        self.do_not_track = True

        self.send_referrer = False

        self.ask_download_path = True

        self.download_directory = ""

        self.overwrite_existing = False

        self.open_links_in_background = False

        self.confirm_before_closing = True

        self.show_tab_close_button = True

        self.dns_prefetch = True

        self.use_system_proxy = True

        self.enable_vpn = False

        self.enable_gpu = True

        self.enable_cache = False

        self.max_cache_size_mb = 128

        self.lazy_load_tabs = True

        self.developer_tools = False

        self.verbose_logging = False

        self.touch()