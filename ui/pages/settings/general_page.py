"""
MRGpt Browser

General Settings Page
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QFormLayout,
    QVBoxLayout,
)

from services.settings_service import SettingsService

from ui.pages.settings.base_settings_page import BaseSettingsPage


class GeneralPage(BaseSettingsPage):
    """
    General browser settings.
    """

    # -------------------------------------------------

    def __init__(
        self,
        settings: SettingsService,
        parent=None,
    ) -> None:

        super().__init__(
    settings,
    parent,
)

        self._create_widgets()

        self._build_ui()

        self.load()

    # -------------------------------------------------

    def _create_widgets(self) -> None:

        self.language = QComboBox()

        self.language.addItems(
            [
                "fa-IR",
                "en-US",
            ]
        )

        self.home_page = QLineEdit()

        self.startup = QComboBox()

        self.startup.addItems(
            [
                "Home Page",
                "Restore Session",
                "Blank Page",
            ]
        )

        self.restore_session = QCheckBox(
            "Restore previous tabs"
        )

    # -------------------------------------------------

    def _build_ui(self) -> None:

        layout = QVBoxLayout(self)

        form = QFormLayout()

        form.addRow(
            QLabel("Language"),
            self.language,
        )

        form.addRow(
            QLabel("Home Page"),
            self.home_page,
        )

        form.addRow(
            QLabel("Startup"),
            self.startup,
        )

        form.addRow(
            "",
            self.restore_session,
        )

        layout.addLayout(form)

        layout.addStretch()

    # -------------------------------------------------

    def load(self) -> None:

        """
        Load settings into controls.
        """

        self.language.setCurrentText(
            self.settings.language
        )

        self.home_page.setText(
            self.settings.home_page
        )

        startup = self.settings.startup_mode

        index = self.startup.findText(
            startup
        )

        if index >= 0:

            self.startup.setCurrentIndex(
                index
            )

        self.restore_session.setChecked(

    self.settings.restore_session

)

    # -------------------------------------------------

    def apply(self) -> None:

        """
        Save changes.
        """

        self.settings.language = (
            self.language.currentText()
        )

        self.settings.home_page = (
            self.home_page.text().strip()
        )

        self.settings.startup_mode = (

    self.startup.currentText()

)

        self.settings.restore_session = (
        
        self.restore_session.isChecked()

        )
        self.settings.sync()
    
    
    def validate(self) -> bool:

        if not self.home_page.text().strip():
        
            return False
    
        return True