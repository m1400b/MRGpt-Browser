"""
MRGpt Browser

Base Settings Page
"""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

from services.settings_service import SettingsService


class BaseSettingsPage(QWidget):
    """
    Base class for settings pages.

    All settings pages receive the shared
    SettingsService instance.
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

    def load(self) -> None:
        """
        Load settings into the page controls.

        Subclasses should override this method.
        """
        pass

    # -------------------------------------------------

    def apply(self) -> None:
        """
        Apply settings from the page controls.

        Subclasses should override this method.
        """
        pass

    # -------------------------------------------------

    def validate(self) -> bool:
        """
        Validate page settings.

        Returns
        -------
        bool
            True when settings are valid.
        """

        return True

    # -------------------------------------------------

    def save_settings(self) -> None:
        """
        Validate and apply page settings.
        """

        if not self.validate():
            return

        self.apply()

        self.settings.sync()

