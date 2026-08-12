"""
MRGpt Browser

Base Browser Profile
"""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal
from PySide6.QtWebEngineCore import (
    QWebEngineProfile,
    QWebEngineSettings,
)


class BrowserProfile(QObject):

    download_requested = Signal(object)

    def __init__(
        self,
        name: str = "Default",
        parent=None,
    ):

        super().__init__(parent)

        self._name = name

        self._profile = QWebEngineProfile(
            self
        )

        self._configure()

        self._profile.downloadRequested.connect(
            self._on_download_requested
        )

        print(
            "PROFILE CREATED:",
            self._profile
        )

    # -------------------------------------------------

    def _on_download_requested(
        self,
        request,
    ):

        print(
            "🔥 PROFILE DOWNLOAD REQUEST:"
        )

        print(
            "URL:",
            request.url().toString()
        )

        print(
            "FILE:",
            request.downloadFileName()
        )

        self.download_requested.emit(
            request
        )

    # -------------------------------------------------

    def _configure(self):

        self._profile.settings().setAttribute(
            QWebEngineSettings.JavascriptEnabled,
            True
        )

        self._profile.settings().setAttribute(
            QWebEngineSettings.AutoLoadImages,
            True
        )

        self._profile.settings().setAttribute(
            QWebEngineSettings.PdfViewerEnabled,
            True
        )

        self._profile.settings().setAttribute(
            QWebEngineSettings.FullScreenSupportEnabled,
            True
        )

        self._profile.setHttpAcceptLanguage(
            "fa-IR,fa,en-US,en"
        )

    # -------------------------------------------------

    @property
    def qt_profile(self):

        return self._profile

    # -------------------------------------------------

    @property
    def name(self):

        return self._name

    # -------------------------------------------------

    def clear(self):

        self._profile.cookieStore().deleteAllCookies()

        self._profile.clearHttpCache()