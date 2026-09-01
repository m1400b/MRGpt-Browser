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
    """Browser facade and navigation/history integration point."""

    title_changed = Signal(str)
    url_changed = Signal(QUrl)
    current_tab_changed = Signal()
    load_started = Signal()
    load_progress = Signal(int)
    load_finished = Signal(bool)

    def __init__(self, services: ServiceContainer, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.services = services
        self.profile_service = services.resolve(ServiceNames.PROFILE)
        self.browser_service = services.resolve(ServiceNames.BROWSER)
        self.download_manager = services.resolve(ServiceNames.DOWNLOADS)
        self.history_service = services.resolve(ServiceNames.HISTORY)
        self._connected_tab = None

        profile = self.profile_service.current()
        self.tabs = TabWidget(profile, self)

        self._build_ui()
        self._connect()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.tabs)

    def _connect(self) -> None:
        self.tabs.tab_created.connect(self.browser_service.add_tab)
        self.tabs.tab_created.connect(self._connect_download_signal)
        self.tabs.tab_closed.connect(self.browser_service.remove_tab)
        self.tabs.current_tab_changed.connect(self._current_tab_changed)
        self.tabs.new_tab_requested.connect(self.new_tab)

        self.browser_service.title_changed.connect(self.title_changed.emit)
        self.browser_service.url_changed.connect(self.url_changed.emit)

        # Record history only after a successful page load.
        # HistoryService itself enforces privacy/save_history.
        self.load_finished.connect(self._record_history)

        self._connect_current_tab()

    def _record_history(self, ok: bool) -> None:
        if not ok:
            return

        self.history_service.record_navigation(
            self.current_url(),
            self.current_title(),
        )

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

    def _connect_current_tab(self) -> None:
        self._disconnect_current_tab()
        tab = self.current_tab
        if tab is None:
            return

        tab.load_started.connect(self.load_started.emit)
        tab.load_progress.connect(self.load_progress.emit)
        tab.load_finished.connect(self.load_finished.emit)
        self._connected_tab = tab

    def _current_tab_changed(self, *args) -> None:
        self.browser_service.set_current_tab(self.current_tab)
        self._connect_current_tab()
        self.url_changed.emit(self.current_url())
        self.title_changed.emit(self.current_title())
        self.current_tab_changed.emit()

    def navigate(self, url: str | QUrl) -> None:
        if isinstance(url, str):
            url = QUrl(url)

        tab = self.current_tab
        if tab is None:
            return

        tab.load(url)

    def load_url(self, url: str | QUrl) -> None:
        self.navigate(url)

    def new_tab(self, url: QUrl | None = None) -> None:
        self.tabs.create_tab(url)

    def close_current_tab(self) -> None:
        self.tabs.close_current_tab()

    def duplicate_tab(self) -> None:
        self.tabs.duplicate_current_tab()

    def reload(self) -> None:
        self.tabs.reload_current_tab()

    def stop(self) -> None:
        self.tabs.stop_loading()

    def back(self) -> None:
        self.tabs.back()

    def forward(self) -> None:
        self.tabs.forward()

    def zoom_in(self) -> None:
        self.tabs.zoom_in()

    def zoom_out(self) -> None:
        self.tabs.zoom_out()

    def reset_zoom(self) -> None:
        self.tabs.reset_zoom()

    def current_url(self) -> QUrl:
        tab = self.current_tab
        if tab:
            return tab.url
        return QUrl()

    def current_title(self) -> str:
        tab = self.current_tab
        if tab:
            return tab.title
        return ""

    def can_go_back(self) -> bool:
        view = self.current_view
        return bool(view and view.history().canGoBack())

    def can_go_forward(self) -> bool:
        view = self.current_view
        return bool(view and view.history().canGoForward())

    def is_loading(self) -> bool:
        view = self.current_view
        return bool(view and view.isLoading())

    @property
    def current_tab(self):
        return self.tabs.current_tab()

    @property
    def current_view(self):
        return self.tabs.current_view()

    @property
    def current_page(self):
        return self.tabs.current_page()

    @property
    def current_profile(self):
        return self.tabs.current_profile()

    def _connect_download_signal(self, tab) -> None:
        if tab is None:
            return
        tab.download_requested.connect(self._handle_download)

    def _handle_download(self, request) -> None:
        if request is None:
            return

        print("🔥 BROWSER DOWNLOAD RECEIVED:")
        print("URL:", request.url().toString())
        print("FILE:", request.downloadFileName())
        self.download_manager.handle_download(request)

    def shutdown(self) -> None:
        self._disconnect_current_tab()

        if self.tabs is not None:
            self.tabs.close_all_tabs()

        try:
            self.browser_service.set_current_tab(None)
        except (RuntimeError, TypeError, AttributeError):
            pass
