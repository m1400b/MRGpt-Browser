"""
MRGpt Browser

Browser Controller
"""

from __future__ import annotations

from PySide6.QtCore import QObject, QUrl

from ui.widgets.tab_widget import TabWidget


class BrowserController(QObject):
    """
    Browser Controller

    Executes all browser commands.

    هیچ وابستگی به UI ندارد.
    """

    # ---------------------------------------------------------

    def __init__(
        self,
        tabs: TabWidget,
        parent: QObject | None = None,
    ) -> None:

        super().__init__(parent)

        self.tabs = tabs

    # =========================================================
    # Navigation
    # =========================================================

    def navigate(
    self,
    url: str | QUrl,
) -> None:

        print("Controller navigate input:", url)
    
        tab = self.tabs.current_tab()
    
        if tab is None:
            return
    
        if isinstance(url, str):
            url = self.prepare_url(url)
    
        print("Prepared URL:", url.toString())
    
        if not url.isValid():
            print("INVALID URL")
            return
    
        tab.load(url)

    # ---------------------------------------------------------

    def prepare_url(
    self,
    text: str,
) -> QUrl:

        text = text.strip()

        if not text:
            return QUrl("about:blank")

        #
        # URL کامل
        #

        if "://" in text:
            return QUrl(text)

        #
        # آدرس‌های محلی یا پورت‌دار
        #

        if ":" in text:
            return QUrl(f"https://{text}")

        #
        # دامنه
        #

        if "." in text:
            return QUrl(f"https://{text}")

        #
        # جستجوی گوگل
        #

        query = text.replace(" ", "+")

        return QUrl(
            f"https://www.google.com/search?q={query}"
        )

    # =========================================================
    # Tab Commands
    # =========================================================

    def new_tab(
        self,
        url: QUrl | None = None,
    ) -> None:

        self.tabs.create_tab(url)

    # ---------------------------------------------------------

    def close_current_tab(self) -> None:

        self.tabs.close_current_tab()

    # ---------------------------------------------------------

    def duplicate_current_tab(self) -> None:

        self.tabs.duplicate_current_tab()

    # =========================================================
    # Navigation Commands
    # =========================================================

    def reload(self) -> None:

        self.tabs.reload_current_tab()

    # ---------------------------------------------------------

    def stop(self) -> None:

        self.tabs.stop_loading()

    # ---------------------------------------------------------

    def back(self) -> None:

        self.tabs.back()

    # ---------------------------------------------------------

    def forward(self) -> None:

        self.tabs.forward()

    # =========================================================
    # Zoom
    # =========================================================

    def zoom_in(self) -> None:

        self.tabs.zoom_in()

    # ---------------------------------------------------------

    def zoom_out(self) -> None:

        self.tabs.zoom_out()

    # ---------------------------------------------------------

    def reset_zoom(self) -> None:

        self.tabs.reset_zoom()