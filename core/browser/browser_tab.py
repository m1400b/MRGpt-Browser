"""
MRGpt Browser

Browser Tab
"""

from __future__ import annotations

from PySide6.QtCore import (
    Signal,
    QUrl,
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from core.browser.browser_view import BrowserView


class BrowserTab(QWidget):

    # -------------------------------------------------
    # Signals
    # -------------------------------------------------

    close_requested = Signal()

    title_changed = Signal(str)

    url_changed = Signal(QUrl)

    icon_changed = Signal()

    load_started = Signal()

    load_finished = Signal(bool)

    load_progress = Signal(int)

    new_tab_requested = Signal(QUrl)

    download_requested = Signal(object)

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------

    def __init__(
        self,
        profile,
        parent=None,
    ):

        super().__init__(parent)

        self.browser = BrowserView(
            profile,
            self,
        )

        self._build_ui()

        self._connect_signals()

    # =================================================
    # UI
    # =================================================

    def _build_ui(self):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.addWidget(
            self.browser
        )

    # =================================================
    # Signals
    # =================================================

    def _connect_signals(self):

        self.browser.close_requested.connect(
            self.close_requested.emit
        )

        self.browser.title_changed.connect(
            self.title_changed.emit
        )

        self.browser.url_changed.connect(
            self.url_changed.emit
        )

        self.browser.load_started.connect(
            self.load_started.emit
        )

        self.browser.load_finished.connect(
            self.load_finished.emit
        )

        self.browser.load_progress.connect(
            self.load_progress.emit
        )

        self.browser.new_tab_requested.connect(
            self.new_tab_requested.emit
        )

        self.browser.download_requested.connect(
            self.download_requested.emit
        )

    # =================================================
    # Navigation
    # =================================================

    def load(
        self,
        url,
    ):

        self.browser.open_url(
            url
        )

    # -------------------------------------------------

    def reload(self):

        self.browser.reload()

    # -------------------------------------------------

    def back(self):

        self.browser.back()

    # -------------------------------------------------

    def forward(self):

        self.browser.forward()

    # -------------------------------------------------

    def stop(self):

        self.browser.stop()

    # =================================================
    # Properties
    # =================================================

    @property
    def url(self):

        return self.browser.current_url()

    # -------------------------------------------------

    @property
    def title(self):

        return self.browser.current_title()

    # =================================================
    # Zoom
    # =================================================

    def zoom_in(self):

        self.browser.zoom_in()

    # -------------------------------------------------

    def zoom_out(self):

        self.browser.zoom_out()

    # -------------------------------------------------

    def reset_zoom(self):

        self.browser.reset_zoom()

    # =================================================
    # Browser Objects
    # =================================================

    @property
    def view(self):

        return self.browser

    # -------------------------------------------------

    @property
    def page(self):

        return self.browser.page()

    # -------------------------------------------------

    @property
    def profile(self):

        page = self.browser.page()

        if page is None:

            return None

        return page.profile()

    # -------------------------------------------------

    @property
    def is_loading(self):

        return self.browser.isLoading()

    # -------------------------------------------------

    @property
    def zoom_factor(self):

        return self.browser.zoomFactor()

    # =================================================
    # Shutdown
    # =================================================

    def close(self) -> None:
        """
        Safely close this browser tab.
    
        BrowserView owns the WebEngine page.
        Cleanup is delegated to BrowserView.
        """
    
        browser = self.browser
    
        if browser is None:
            return
    
        try:
            browser.stop()
    
        except (
            RuntimeError,
            AttributeError,
        ):
            pass
        
        try:
            browser.shutdown()
    
        except (
            RuntimeError,
            AttributeError,
        ):
            pass
        
        
    # -------------------------------------------------
    
    def shutdown(self) -> None:
        """
        Compatibility alias for application shutdown.
        """
    
        self.close()