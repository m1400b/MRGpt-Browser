"""
MRGpt Browser

Browser Service
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QObject, Signal, QUrl

from core.browser.browser_tab import BrowserTab


class BrowserService(QObject):
    """
    Browser Service

    مسئول مدیریت تب‌های مرورگر
    """

    tab_created = Signal(BrowserTab)

    tab_closed = Signal(BrowserTab)

    current_tab_changed = Signal(BrowserTab)

    url_changed = Signal(QUrl)

    title_changed = Signal(str)

    # ----------------------------------------------------

    def __init__(self, parent=None):

        super().__init__(parent)

        self._tabs: list[BrowserTab] = []

        self._current: Optional[BrowserTab] = None

    # ----------------------------------------------------

    def add_tab(self, tab: BrowserTab):

        if tab in self._tabs:
            return

        self._tabs.append(tab)

        self._connect_tab(tab)

        self.set_current_tab(tab)

        self.tab_created.emit(tab)

    # ----------------------------------------------------

    def remove_tab(self, tab: BrowserTab):

        if tab not in self._tabs:
            return

        self._tabs.remove(tab)

        self.tab_closed.emit(tab)

        if self._current is tab:

            self._current = self._tabs[-1] if self._tabs else None

            if self._current:

                self.current_tab_changed.emit(self._current)

    # ----------------------------------------------------

    def set_current_tab(self, tab: BrowserTab):

        if tab not in self._tabs:
            return

        self._current = tab

        self.current_tab_changed.emit(tab)

    # ----------------------------------------------------

    def current_tab(self) -> Optional[BrowserTab]:

        return self._current

    # ----------------------------------------------------

    def current_url(self) -> str:

        if self._current:

            return self._current.url

        return ""

    # ----------------------------------------------------

    def current_title(self) -> str:

        if self._current:

            return self._current.title

        return ""

    # ----------------------------------------------------

    def tabs(self) -> list[BrowserTab]:

        return self._tabs.copy()

    # ----------------------------------------------------

    def count(self) -> int:

        return len(self._tabs)

    # ----------------------------------------------------

    def clear(self):

        self._tabs.clear()

        self._current = None

    # ----------------------------------------------------

    def back(self):

        if self._current:

            self._current.back()

    # ----------------------------------------------------

    def forward(self):

        if self._current:

            self._current.forward()

    # ----------------------------------------------------

    def reload(self):

        if self._current:

            self._current.reload()

    # ----------------------------------------------------

    def stop(self):

        if self._current:

            self._current.stop()

    # ----------------------------------------------------

    def zoom_in(self):

        if self._current:

            self._current.zoom_in()

    # ----------------------------------------------------

    def zoom_out(self):

        if self._current:

            self._current.zoom_out()

    # ----------------------------------------------------

    def reset_zoom(self):

        if self._current:

            self._current.reset_zoom()

    # ----------------------------------------------------

    def load(self, url: str | QUrl):

        if self._current:

            self._current.load(url)

    # ----------------------------------------------------

    def _connect_tab(self, tab: BrowserTab):

        tab.url_changed.connect(

            self.url_changed.emit

        )

        tab.title_changed.connect(

            self.title_changed.emit

        )