"""
MRGpt Browser

Browser Facade
"""

from __future__ import annotations

from PySide6.QtCore import QUrl, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout

from services.service_container import ServiceContainer
from services.service_names import ServiceNames

from ui.widgets.tab_widget import TabWidget


class Browser(QWidget):
    """
    Browser Facade.

    Responsibilities
    ----------------
    - Manage TabWidget
    - Expose browser operations
    - Forward browser signals
    - Hide internal browser implementation
    """

    # -------------------------------------------------
    # Signals
    # -------------------------------------------------

    title_changed = Signal(str)

    url_changed = Signal(QUrl)

    current_tab_changed = Signal()

    load_started = Signal()

    load_progress = Signal(int)

    load_finished = Signal(bool)

    # -------------------------------------------------

    def __init__(
        self,
        services: ServiceContainer,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.services = services

        self.profile_service = services.resolve(
            ServiceNames.PROFILE
        )

        self.browser_service = services.resolve(
            ServiceNames.BROWSER
        )

        self._connected_tab = None

        profile = self.profile_service.current()

        self.tabs = TabWidget(profile)

        self._build_ui()

        self._connect()

        self.tabs.create_tab()

    # -------------------------------------------------

    def _build_ui(self) -> None:

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(0)

        layout.addWidget(
            self.tabs
        )

    # -------------------------------------------------

    def _connect(self) -> None:

        #
        # TabWidget
        #

        self.tabs.tab_created.connect(
            self.browser_service.add_tab
        )

        self.tabs.tab_closed.connect(
            self.browser_service.remove_tab
        )

        self.tabs.current_tab_changed.connect(
            self._current_tab_changed
        )

        self.tabs.new_tab_requested.connect(
            self.new_tab
        )

        #
        # BrowserService
        #

        self.browser_service.title_changed.connect(
            self.title_changed.emit
        )

        self.browser_service.url_changed.connect(
            self.url_changed.emit
        )

        #
        # First Tab
        #

        self._connect_current_tab()

    # -------------------------------------------------

    def _disconnect_current_tab(self) -> None:

        tab = self._connected_tab

        if tab is None:

            return

        for signal, slot in (

            (tab.load_started, self.load_started.emit),

            (tab.load_progress, self.load_progress.emit),

            (tab.load_finished, self.load_finished.emit),

        ):

            try:

                signal.disconnect(slot)

            except (RuntimeError, TypeError):

                pass

        self._connected_tab = None

    # -------------------------------------------------

    def _connect_current_tab(self) -> None:

        self._disconnect_current_tab()

        tab = self.current_tab

        if tab is None:

            return

        tab.load_started.connect(

            self.load_started.emit

        )

        tab.load_progress.connect(

            self.load_progress.emit

        )

        tab.load_finished.connect(

            self.load_finished.emit

        )

        self._connected_tab = tab

    # -------------------------------------------------

    def _current_tab_changed(self) -> None:

        self.browser_service.set_current_tab(

            self.current_tab

        )

        self._connect_current_tab()

        self.url_changed.emit(

            self.current_url()

        )

        self.title_changed.emit(

            self.current_title()

        )

        self.current_tab_changed.emit()

    # -------------------------------------------------

    def navigate(
        self,
        url: str | QUrl,
    ) -> None:

        if isinstance(url, str):

            url = QUrl(url)

        tab = self.current_tab

        if tab is None:

            return

        tab.load(url)

    # -------------------------------------------------

    def load_url(
        self,
        url: str | QUrl,
    ) -> None:

        self.navigate(url)

    # -------------------------------------------------

    def new_tab(
        self,
        url: QUrl | None = None,
    ) -> None:

        self.tabs.create_tab(url)

    # -------------------------------------------------

    def close_current_tab(self) -> None:

        self.tabs.close_current_tab()

    # -------------------------------------------------

    def duplicate_tab(self) -> None:

        self.tabs.duplicate_current_tab()

    # -------------------------------------------------

    def reload(self) -> None:

        self.tabs.reload_current_tab()

    # -------------------------------------------------

    def stop(self) -> None:

        self.tabs.stop_loading()

    # -------------------------------------------------

    def back(self) -> None:

        self.tabs.back()

    # -------------------------------------------------

    def forward(self) -> None:

        self.tabs.forward()

    # -------------------------------------------------

    def zoom_in(self) -> None:

        self.tabs.zoom_in()

    # -------------------------------------------------

    def zoom_out(self) -> None:

        self.tabs.zoom_out()

    # -------------------------------------------------

    def reset_zoom(self) -> None:

        self.tabs.reset_zoom()

    # -------------------------------------------------

    def current_url(self) -> QUrl:

        tab = self.current_tab

        return tab.url if tab else QUrl()

    # -------------------------------------------------

    def current_title(self) -> str:

        tab = self.current_tab

        return tab.title if tab else ""

    # -------------------------------------------------

    def can_go_back(self) -> bool:

        view = self.current_view

        return bool(

            view and

            view.history().canGoBack()

        )

    # -------------------------------------------------

    def can_go_forward(self) -> bool:

        view = self.current_view

        return bool(

            view and

            view.history().canGoForward()

        )

    # -------------------------------------------------

    def is_loading(self) -> bool:

        view = self.current_view

        return bool(

            view and

            view.isLoading()

        )

    # -------------------------------------------------

    @property
    def current_tab(self):

        return self.tabs.current_tab()

    # -------------------------------------------------

    @property
    def current_view(self):

        return self.tabs.current_view()

    # -------------------------------------------------

    @property
    def current_page(self):

        return self.tabs.current_page()

    # -------------------------------------------------

    @property
    def current_profile(self):

        return self.tabs.current_profile()