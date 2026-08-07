"""
MRGpt Browser

Base Browser Profile
"""

from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtWebEngineCore import (
    QWebEngineProfile,
    QWebEngineSettings,
)


class BrowserProfile(QObject):

    def __init__(self, name: str = "Default", parent=None):

        super().__init__(parent)

        self._name = name

        self._profile = QWebEngineProfile(self)

        self._configure()

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