"""
MRGpt Browser

Downloads Settings Page
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QVBoxLayout,
)

from services.settings_service import SettingsService

from ui.pages.settings.base_settings_page import BaseSettingsPage


class DownloadsPage(BaseSettingsPage):
    """
    Download settings page.
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

        self._connect_signals()

        self.load()

    # =================================================
    # UI
    # =================================================

    def _create_widgets(self) -> None:

        self.download_path = QLineEdit()

        self.browse_button = QPushButton(
            "Browse..."
        )

        self.ask_location = QCheckBox(
            "Ask where to save each file"
        )

        self.open_after_download = QCheckBox(
            "Open downloaded files automatically"
        )

    # -------------------------------------------------

    def _build_ui(self) -> None:

        layout = QVBoxLayout(
            self
        )

        form = QFormLayout()

        # ---------------------------------------------
        # Download location
        # ---------------------------------------------

        path_layout = QHBoxLayout()

        path_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        path_layout.addWidget(
            self.download_path,
            1,
        )

        path_layout.addWidget(
            self.browse_button
        )

        form.addRow(
            QLabel("Download location"),
            path_layout,
        )

        # ---------------------------------------------
        # Options
        # ---------------------------------------------

        form.addRow(
            "",
            self.ask_location,
        )

        form.addRow(
            "",
            self.open_after_download,
        )

        layout.addLayout(
            form
        )

        layout.addStretch()

    # -------------------------------------------------

    def _connect_signals(self) -> None:

        self.browse_button.clicked.connect(
            self._browse_download_path
        )

    # =================================================
    # Browse
    # =================================================

    def _browse_download_path(self) -> None:

        path = QFileDialog.getExistingDirectory(
            self,
            "Select Download Folder",
            self.download_path.text(),
        )

        if path:

            self.download_path.setText(
                path
            )

    # =================================================
    # Settings
    # =================================================

    def load(self) -> None:

        """
        Load download settings into controls.
        """

        self.download_path.setText(
            self.settings.download_path
        )

        self.ask_location.setChecked(
            self.settings.ask_download_location
        )

        self.open_after_download.setChecked(
            self.settings.open_after_download
        )

    # -------------------------------------------------

    def apply(self) -> None:

        """
        Save download settings.
        """

        self.settings.download_path = (
            self.download_path.text().strip()
        )

        self.settings.ask_download_location = (
            self.ask_location.isChecked()
        )

        self.settings.open_after_download = (
            self.open_after_download.isChecked()
        )

    # -------------------------------------------------

    def validate(self) -> bool:

        return bool(
            self.download_path.text().strip()
        )