"""
MRGpt Browser

Private Profile
"""

from __future__ import annotations

from PySide6.QtWebEngineCore import QWebEngineProfile

from core.profile.browser_profile import BrowserProfile


class PrivateProfile(BrowserProfile):

    def __init__(self):

        super().__init__("Private")

        profile = self.qt_profile

        profile.setHttpCacheType(
            QWebEngineProfile.MemoryHttpCache
        )

        profile.setPersistentCookiesPolicy(
            QWebEngineProfile.NoPersistentCookies
        )

        profile.setCachePath("")

        profile.setPersistentStoragePath("")