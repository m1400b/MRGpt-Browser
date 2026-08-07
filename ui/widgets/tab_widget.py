"""
MRGpt Browser

Tab Manager Widget
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtCore import QUrl

from PySide6.QtWidgets import (
    QTabWidget,
)

from core.browser.browser_tab import BrowserTab


class TabWidget(QTabWidget):
    """
    تمام مدیریت تب‌ها در این کلاس انجام می‌شود.
    """

    # --------------------------------------------------

    current_tab_changed = Signal(BrowserTab)

    tab_created = Signal(BrowserTab)

    tab_closed = Signal(int)

    new_tab_requested = Signal(QUrl)

    # --------------------------------------------------

    def __init__(self, profile, parent=None):

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

    # --------------------------------------------------

    def create_tab(

        self,

        url: str | QUrl | None = None,

        title: str = "New Tab"

    ) -> BrowserTab:

        tab = BrowserTab(self.profile)

        index = self.addTab(tab, title)

        self.setCurrentIndex(index)

        self._connect_tab(tab)

        if url:

            tab.load(url)

        self.tab_created.emit(tab)

        return tab

    # --------------------------------------------------

    def _connect_tab(
        self,
        tab: BrowserTab
    ):

        tab.title_changed.connect(

            lambda text, t=tab:

            self.setTabText(

                self.indexOf(t),

                text

            )

        )

        tab.icon_changed.connect(

            lambda t=tab:

            self.setTabIcon(

                self.indexOf(t),

                t.view.icon()

            )

        )

        tab.new_tab_requested.connect(

            self.new_tab_requested.emit

        )

    # --------------------------------------------------

    def close_tab(
        self,
        index: int
    ):

        if self.count() == 1:

            return

        widget = self.widget(index)

        widget.deleteLater()

        self.removeTab(index)

        self.tab_closed.emit(index)

    # --------------------------------------------------

    def duplicate_current_tab(self):

        tab = self.current_tab()

        if tab is None:
            return

        self.create_tab(tab.url)

    # --------------------------------------------------

    def current_tab(self) -> Optional[BrowserTab]:

        widget = self.currentWidget()

        if isinstance(widget, BrowserTab):

            return widget

        return None

    # --------------------------------------------------

    def current_view(self):

        tab = self.current_tab()

        if tab:

            return tab.view

        return None

    # --------------------------------------------------

    def current_page(self):

        tab = self.current_tab()

        if tab:

            return tab.page

        return None

    # --------------------------------------------------

    def current_profile(self):

        tab = self.current_tab()

        if tab:

            return tab.profile

        return None

    # --------------------------------------------------

    def _current_changed(self, index):

        tab = self.widget(index)

        if isinstance(tab, BrowserTab):

            self.current_tab_changed.emit(tab)

    # --------------------------------------------------

    def next_tab(self):

        if self.count() == 0:
            return

        index = (self.currentIndex() + 1) % self.count()

        self.setCurrentIndex(index)

    # --------------------------------------------------

    def previous_tab(self):

        if self.count() == 0:
            return

        index = self.currentIndex() - 1

        if index < 0:

            index = self.count() - 1

        self.setCurrentIndex(index)

    # --------------------------------------------------

    def close_current_tab(self):

        self.close_tab(

            self.currentIndex()

        )

    # --------------------------------------------------

    def reload_current_tab(self):

        tab = self.current_tab()

        if tab:

            tab.reload()

    # --------------------------------------------------

    def stop_loading(self):

        tab = self.current_tab()

        if tab:

            tab.stop()

    # --------------------------------------------------

    def back(self):

        tab = self.current_tab()

        if tab:

            tab.back()

    # --------------------------------------------------

    def forward(self):

        tab = self.current_tab()

        if tab:

            tab.forward()

    # --------------------------------------------------

    def zoom_in(self):

        tab = self.current_tab()

        if tab:

            tab.zoom_in()

    # --------------------------------------------------

    def zoom_out(self):

        tab = self.current_tab()

        if tab:

            tab.zoom_out()

    # --------------------------------------------------

    def reset_zoom(self):

        tab = self.current_tab()

        if tab:

            tab.reset_zoom()