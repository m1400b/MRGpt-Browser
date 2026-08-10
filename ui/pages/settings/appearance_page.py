"""
MRGpt Browser

Appearance Settings Page
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QVBoxLayout,
)

from PySide6.QtCore import Qt
from services.settings_service import SettingsService

from ui.pages.settings.base_settings_page import BaseSettingsPage


class AppearancePage(BaseSettingsPage):
    """
    Appearance settings.
    """

    # -------------------------------------------------

    def __init__(
    self,
    settings: SettingsService,
    appearance,
    parent=None,
) -> None:

        super().__init__(
            settings,
            parent,
        )
        
        self.appearance = appearance

        self._create_widgets()

        self._build_ui()

        self.load()

    # =================================================
    # Widgets
    # =================================================

    def _create_widgets(self) -> None:

        #
        # Theme
        #

        self.theme = QComboBox()

        self.theme.addItems(
            [
                "System",
                "Light",
                "Dark",
            ]
        )

        #
        # Zoom
        #

        self.zoom_factor = QDoubleSpinBox()

        self.zoom_factor.setRange(
            0.50,
            3.00,
        )

        self.zoom_factor.setSingleStep(
            0.10
        )

        self.zoom_factor.setDecimals(
            2
        )

        #
        # UI Scale
        #

        self.ui_scale = QDoubleSpinBox()

        self.ui_scale.setRange(
            0.75,
            2.00,
        )

        self.ui_scale.setSingleStep(
            0.05
        )

        self.ui_scale.setDecimals(
            2
        )

        #
        # Status Bar
        #

        self.show_status_bar = QCheckBox(
            "Show status bar"
        )

        #
        # Bookmark Bar
        #

        self.show_bookmark_bar = QCheckBox(
            "Show bookmark bar"
        )

    # =================================================
    # UI
    # =================================================

    def _build_ui(self) -> None:

        layout = QVBoxLayout(
            self
        )

        appearance_group = QGroupBox(
            "Appearance"
        )

        form = QFormLayout(
            appearance_group
        )

        form.addRow(
            "Theme",
            self.theme,
        )

        form.addRow(
            "Zoom Factor",
            self.zoom_factor,
        )

        form.addRow(
            "UI Scale",
            self.ui_scale,
        )

        form.addRow(
            "",
            self.show_status_bar,
        )

        form.addRow(
            "",
            self.show_bookmark_bar,
        )

        layout.addWidget(
            appearance_group
        )

        layout.addStretch()

    # =================================================
    # Load
    # =================================================

    def load(self) -> None:
        """
        Load appearance settings into controls.
        """

        #
        # Theme
        #

        theme = self.settings.theme

        index = self.theme.findText(
            theme,
            Qt.MatchFixedString,
        )

        if index >= 0:

            self.theme.setCurrentIndex(
                index
            )

        #
        # Zoom
        #

        self.zoom_factor.setValue(
            self.settings.zoom_factor
        )

        #
        # UI Scale
        #

        self.ui_scale.setValue(
            float(
                self.settings.value(
                    "appearance/ui_scale",
                    1.0,
                )
            )
        )

        #
        # Status Bar
        #

        self.show_status_bar.setChecked(
            bool(
                self.settings.value(
                    "appearance/show_status_bar",
                    True,
                )
            )
        )

        #
        # Bookmark Bar
        #

        self.show_bookmark_bar.setChecked(
            bool(
                self.settings.value(
                    "appearance/show_bookmark_bar",
                    False,
                )
            )
        )

    # =================================================
    # Apply
    # =================================================

    def apply(self) -> None:
        """
        Save appearance settings.
        """

        #
        # Theme
        #

        self.settings.theme = (
            self.theme.currentText()
        )
        

        #
        # Zoom
        #

        self.settings.zoom_factor = (
            self.zoom_factor.value()
        )

        #
        # UI Scale
        #

        self.settings.set_value(
            "appearance/ui_scale",
            self.ui_scale.value(),
        )

        #
        # Status Bar
        #

        self.settings.set_value(
            "appearance/show_status_bar",
            self.show_status_bar.isChecked(),
        )

        #
        # Bookmark Bar
        #

        self.settings.set_value(
            "appearance/show_bookmark_bar",
            self.show_bookmark_bar.isChecked(),
        )

    # =================================================
    # Validate
    # =================================================

    def validate(self) -> bool:
        """
        Validate appearance settings.
        """

        return (
            0.50
            <= self.zoom_factor.value()
            <= 3.00
            and
            0.75
            <= self.ui_scale.value()
            <= 2.00
        )

