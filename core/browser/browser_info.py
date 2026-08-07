"""
MRGpt Browser

Browser Information
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import (
    qVersion,
)

from PySide6.QtWebEngineCore import (
    qWebEngineChromiumVersion,
)


@dataclass(slots=True, frozen=True)
class BrowserInfo:
    """
    Static browser information.
    """

    application_name: str = "MRGpt Browser"

    application_version: str = "0.6.0"

    chromium_version: str = qWebEngineChromiumVersion()

    qt_version: str = qVersion()

    platform: str = "Windows"

    language: str = "fa-IR"

    @property
    def user_agent(self) -> str:

        return (

            f"Mozilla/5.0 "
            f"(Windows NT 10.0; Win64; x64) "
            f"AppleWebKit/537.36 "
            f"(KHTML, like Gecko) "
            f"Chrome/{self.chromium_version} "
            f"Safari/537.36"

        )