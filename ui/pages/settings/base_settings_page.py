"""
MRGpt Browser

Base Settings Page
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from PySide6.QtWidgets import QWidget

from services.settings_service import SettingsService


class BaseSettingsPage(QWidget, ABC):
    """
    Base class for all settings pages.

    تمام صفحات تنظیمات باید از این کلاس
    ارث‌بری کنند.
    """

    # -------------------------------------------------

    def __init__(
        self,
        settings: SettingsService,
        parent=None,
    ) -> None:

        super().__init__(parent)

        self.settings = settings

    # -------------------------------------------------

    @abstractmethod
    def oad_settings(self) -> None:
        """
        Load values from SettingsService
        into UI controls.
        """

        raise NotImplementedError

    # -------------------------------------------------

    @abstractmethod
    def apply_settings(self) -> None:
        """
        Save values from UI controls
        into SettingsService.
        """

        raise NotImplementedError
    
    def validate(self) -> bool:
        """
        Validate page values before saving.
        """
    
        return True