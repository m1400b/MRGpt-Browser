"""
MRGpt Browser

Tab Manager Widget
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Signal, QUrl
from PySide6.QtWidgets import QTabWidget

from core.browser.browser_tab import BrowserTab


class TabWidget(QTabWidget):
    """
    تمام مدیریت تب‌ها در این کلاس انجام می‌شود.
    """

    # -------------------------------------------------
    # Signals
    # -------------------------------------------------

    current_tab_changed = Signal(BrowserTab)

    tab_created = Signal(BrowserTab)

    tab_closed = Signal(BrowserTab)

    new_tab_requested = Signal(QUrl)

    # -------------------------------------------------

    def __init__(
        self,
        profile,
        parent=None,
    ):

        super().__init__(parent)

        self.profile = profile

        self.setDocumentMode(True)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setUsesScrollButtons(True)

        self.currentChanged.connect(
            self._current_changed
        )

        self.tabCloseRequested.connect(
            self.close_tab
        )

    # =================================================
    # Create
    # =================================================

    def create_tab(
        self,
        url: str | QUrl | None = None,
        title: str = "New Tab",
    ) -> BrowserTab:

        tab = BrowserTab(
            self.profile
        )

        index = self.addTab(
            tab,
            title
        )

        self.setCurrentIndex(
            index
        )

        self._connect_tab(
            tab
        )

        if url:
            tab.load(url)

        self.tab_created.emit(
            tab
        )

        return tab

    # =================================================
    # Connect Tab
    # =================================================

    def _connect_tab(
        self,
        tab: BrowserTab,
    ) -> None:

        tab.title_changed.connect(
            lambda text, t=tab:
            self._update_tab_title(
                t,
                text,
            )
        )

        tab.icon_changed.connect(
            lambda t=tab:
            self._update_tab_icon(
                t,
            )
        )

        tab.new_tab_requested.connect(
            self.new_tab_requested.emit
        )

    # -------------------------------------------------

    def _update_tab_title(
        self,
        tab: BrowserTab,
        title: str,
    ) -> None:

        index = self.indexOf(tab)

        if index < 0:
            return

        self.setTabText(
            index,
            title,
        )

    # -------------------------------------------------

    def _update_tab_icon(
        self,
        tab: BrowserTab,
    ) -> None:

        index = self.indexOf(tab)

        if index < 0:
            return

        self.setTabIcon(
            index,
            tab.view.icon(),
        )

    # =================================================
    # Close
    # =================================================

    def close_tab(
        self,
        index: int,
    ) -> None:

        if index < 0:
            return

        if index >= self.count():
            return

        # ---------------------------------------------
        # Keep at least one tab alive
        # ---------------------------------------------

        if self.count() == 1:
            return

        widget = self.widget(
            index
        )

        if not isinstance(
            widget,
            BrowserTab,
        ):
            return

        # ---------------------------------------------
        # Remove from QTabWidget first
        # ---------------------------------------------

        self.removeTab(
            index
        )

        # ---------------------------------------------
        # Notify Browser
        # ---------------------------------------------

        self.tab_closed.emit(
            widget
        )

        # ---------------------------------------------
        # Close BrowserTab
        # ---------------------------------------------

        self._destroy_tab(
            widget
        )

    # -------------------------------------------------

    def _destroy_tab(
        self,
        tab: BrowserTab,
    ) -> None:

        if tab is None:
            return

        # ---------------------------------------------
        # Stop + cleanup WebEngine resources
        # ---------------------------------------------

        try:
            tab.close()

        except (
            RuntimeError,
            AttributeError,
        ):
            pass

        # ---------------------------------------------
        # Destroy BrowserTab after cleanup
        # ---------------------------------------------

        try:
            tab.deleteLater()

        except RuntimeError:
            pass
    
    # =================================================
    # Duplicate
    # =================================================

    def duplicate_current_tab(
        self,
    ) -> None:

        tab = self.current_tab()

        if tab is None:
            return

        self.create_tab(
            tab.url
        )

    # =================================================
    # Current Tab
    # =================================================

    def current_tab(
        self,
    ) -> Optional[BrowserTab]:

        widget = self.currentWidget()

        if isinstance(
            widget,
            BrowserTab,
        ):
            return widget

        return None

    # -------------------------------------------------

    def current_view(self):

        tab = self.current_tab()

        if tab:
            return tab.view

        return None

    # -------------------------------------------------

    def current_page(self):

        tab = self.current_tab()

        if tab:
            return tab.page

        return None

    # -------------------------------------------------

    def current_profile(self):

        tab = self.current_tab()

        if tab:
            return tab.profile

        return None

    # =================================================
    # Current Changed
    # =================================================

    def _current_changed(
        self,
        index,
    ) -> None:

        tab = self.widget(
            index
        )

        if isinstance(
            tab,
            BrowserTab,
        ):

            self.current_tab_changed.emit(
                tab
            )

    # =================================================
    # Navigation
    # =================================================

    def next_tab(self):

        if self.count() == 0:
            return

        index = (
            self.currentIndex() + 1
        ) % self.count()

        self.setCurrentIndex(
            index
        )

    # -------------------------------------------------

    def previous_tab(self):

        if self.count() == 0:
            return

        index = (
            self.currentIndex() - 1
        )

        if index < 0:
            index = self.count() - 1

        self.setCurrentIndex(
            index
        )

    # -------------------------------------------------

    def close_current_tab(self):

        self.close_tab(
            self.currentIndex()
        )

    # -------------------------------------------------

    def reload_current_tab(self):

        tab = self.current_tab()

        if tab:
            tab.reload()

    # -------------------------------------------------

    def stop_loading(self):

        tab = self.current_tab()

        if tab:
            tab.stop()

    # -------------------------------------------------

    def back(self):

        tab = self.current_tab()

        if tab:
            tab.back()

    # -------------------------------------------------

    def forward(self):

        tab = self.current_tab()

        if tab:
            tab.forward()

    # -------------------------------------------------

    def zoom_in(self):

        tab = self.current_tab()

        if tab:
            tab.zoom_in()

    # -------------------------------------------------

    def zoom_out(self):

        tab = self.current_tab()

        if tab:
            tab.zoom_out()

    # -------------------------------------------------

    def reset_zoom(self):

        tab = self.current_tab()

        if tab:
            tab.reset_zoom()

    # =================================================
    # Shutdown
    # =================================================

    def close_all_tabs(
    self,
) -> None:
        """
        Close every BrowserTab during application shutdown.
        """
    
        while self.count() > 0:
        
            widget = self.widget(0)
    
            self.removeTab(0)
    
            if not isinstance(
                widget,
                BrowserTab,
            ):
                continue
            
            # -----------------------------------------
            # Cleanup WebEngine resources
            # -----------------------------------------
    
            self._destroy_tab(
                widget
            )
    
            # -----------------------------------------
            # Notify Browser
            # -----------------------------------------
    
            self.tab_closed.emit(
                widget
            )
    
        self.clear()