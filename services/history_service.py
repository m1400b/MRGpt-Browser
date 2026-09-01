"""
MRGpt Browser

History Service
"""

from __future__ import annotations

from PySide6.QtCore import QObject, QUrl, Signal

from managers.history_manager import HistoryManager
from services.settings_service import SettingsService


class HistoryService(QObject):
    """
    Application history service.

    This is the privacy boundary for browser history:
    no navigation is persisted unless save_history is enabled.
    """

    history_added = Signal(object)

    def __init__(
        self,
        settings_service: SettingsService,
        manager: HistoryManager,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.settings_service = settings_service
        self.manager = manager

    # =========================================================
    # Navigation
    # =========================================================

    def record_navigation(
        self,
        url: QUrl | str,
        title: str = "",
    ) -> None:
        """
        Record a completed navigation when history saving is enabled.
        """

        if not self.settings_service.save_history:
            return

        if isinstance(url, str):
            url = QUrl(url)

        if not isinstance(url, QUrl) or not url.isValid():
            return

        scheme = url.scheme().lower()

        # Do not put internal/non-web pages in normal browsing history.
        if scheme not in {"http", "https"}:
            return

        url_text = url.toString().strip()

        if not url_text:
            return

        item = self.manager.add_visit(
            title=title or url.host() or url_text,
            url=url_text,
        )

        self.history_added.emit(item)

    # =========================================================
    # Management API
    # =========================================================

    def all(self):
        return self.manager.all()

    def recent(self, limit: int = 50):
        return self.manager.recent(limit)

    def search(self, keyword: str):
        return self.manager.search(keyword)

    def count(self):
        return self.manager.count()

    def remove(self, history_id: int):
        return self.manager.remove(history_id)

    def delete_by_url(self, url: str):
        return self.manager.delete_by_url(url)

    def clear(self):
        return self.manager.clear()
