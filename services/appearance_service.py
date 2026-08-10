"""
MRGpt Browser

Appearance Service
"""

from __future__ import annotations

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication, QStyleFactory

from services.settings_service import SettingsService


class AppearanceService:
    """
    Application appearance service.

    مسئول اعمال Theme و تنظیمات ظاهری
    در سطح QApplication است.
    """

    # -------------------------------------------------

    def __init__(
        self,
        settings: SettingsService,
        application: QApplication,
    ) -> None:

        self.settings = settings

        self.application = application

    # =================================================
    # Public API
    # =================================================

    def apply(self) -> None:
        """
        Apply current appearance settings.
        """

        theme = self.settings.theme

        if theme == "Dark":

            self.apply_dark()

        elif theme == "Light":

            self.apply_light()

        else:

            self.apply_system()

    # =================================================
    # Dark
    # =================================================

    def apply_dark(self) -> None:
        """
        Apply a complete dark palette.
        """

        palette = QPalette()

        # ---------------------------------------------
        # Active
        # ---------------------------------------------

        palette.setColor(
            QPalette.Window,
            QColor("#202124"),
        )

        palette.setColor(
            QPalette.WindowText,
            QColor("#F1F3F4"),
        )

        palette.setColor(
            QPalette.Base,
            QColor("#292A2D"),
        )

        palette.setColor(
            QPalette.AlternateBase,
            QColor("#303134"),
        )

        palette.setColor(
            QPalette.ToolTipBase,
            QColor("#303134"),
        )

        palette.setColor(
            QPalette.ToolTipText,
            QColor("#F1F3F4"),
        )

        palette.setColor(
            QPalette.Text,
            QColor("#F1F3F4"),
        )

        palette.setColor(
            QPalette.Button,
            QColor("#303134"),
        )

        palette.setColor(
            QPalette.ButtonText,
            QColor("#F1F3F4"),
        )

        palette.setColor(
            QPalette.BrightText,
            QColor("#FFFFFF"),
        )

        palette.setColor(
            QPalette.Link,
            QColor("#8AB4F8"),
        )

        palette.setColor(
            QPalette.Highlight,
            QColor("#3C78D8"),
        )

        palette.setColor(
            QPalette.HighlightedText,
            QColor("#FFFFFF"),
        )

        # ---------------------------------------------
        # Disabled
        # ---------------------------------------------

        disabled_text = QColor("#80868B")

        palette.setColor(
            QPalette.Disabled,
            QPalette.WindowText,
            disabled_text,
        )

        palette.setColor(
            QPalette.Disabled,
            QPalette.Text,
            disabled_text,
        )

        palette.setColor(
            QPalette.Disabled,
            QPalette.ButtonText,
            disabled_text,
        )

        palette.setColor(
            QPalette.Disabled,
            QPalette.HighlightedText,
            disabled_text,
        )

        # ---------------------------------------------
        # Apply
        # ---------------------------------------------

        self._apply_palette(
            palette
        )

    # =================================================
    # Light
    # =================================================

    def apply_light(self) -> None:
        """
        Apply a complete light palette.
        """

        palette = QPalette()

        # ---------------------------------------------
        # Active
        # ---------------------------------------------

        palette.setColor(
            QPalette.Window,
            QColor("#F5F5F5"),
        )

        palette.setColor(
            QPalette.WindowText,
            QColor("#202124"),
        )

        palette.setColor(
            QPalette.Base,
            QColor("#FFFFFF"),
        )

        palette.setColor(
            QPalette.AlternateBase,
            QColor("#F1F3F4"),
        )

        palette.setColor(
            QPalette.ToolTipBase,
            QColor("#FFFFFF"),
        )

        palette.setColor(
            QPalette.ToolTipText,
            QColor("#202124"),
        )

        palette.setColor(
            QPalette.Text,
            QColor("#202124"),
        )

        palette.setColor(
            QPalette.Button,
            QColor("#F1F3F4"),
        )

        palette.setColor(
            QPalette.ButtonText,
            QColor("#202124"),
        )

        palette.setColor(
            QPalette.BrightText,
            QColor("#000000"),
        )

        palette.setColor(
            QPalette.Link,
            QColor("#1A73E8"),
        )

        palette.setColor(
            QPalette.Highlight,
            QColor("#1A73E8"),
        )

        palette.setColor(
            QPalette.HighlightedText,
            QColor("#FFFFFF"),
        )

        # ---------------------------------------------
        # Apply
        # ---------------------------------------------

        self._apply_palette(
            palette
        )

    # =================================================
    # System
    # =================================================

    def apply_system(self) -> None:
        """
        Restore the platform/application default palette.
        """

        self.application.setPalette(
            self.application.style().standardPalette()
        )

    # =================================================
    # Internal
    # =================================================

    def _apply_palette(
        self,
        palette: QPalette,
    ) -> None:
        """
        Apply palette consistently across the application.
        """

        # Fusion respects QPalette much more consistently
        # across Windows and Qt widgets.

        self.application.setStyle(
            QStyleFactory.create("Fusion")
        )

        self.application.setPalette(
            palette
        )

    # =================================================
    # Convenience
    # =================================================

    def theme(self) -> str:

        return self.settings.theme

    # -------------------------------------------------

    def set_theme(
        self,
        theme: str,
    ) -> None:

        self.settings.theme = theme

        self.settings.sync()

        self.apply()