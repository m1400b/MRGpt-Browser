"""
MRGpt Browser

Download Manager Window
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from services.service_names import ServiceNames
from services.service_container import ServiceContainer

from ui.widgets.downloads.downloads_widget import (
    DownloadsWidget,
)


class DownloadManagerWindow(QDialog):
    """
    Standalone Download Manager window.

    Responsibilities
    ----------------
    - Display the DownloadsWidget
    - Provide a dedicated download manager window
    - Keep the browser UI uncluttered
    """

    # =================================================
    # Constructor
    # =================================================

    def __init__(
        self,
        services: ServiceContainer,
        parent=None,
    ) -> None:

        super().__init__(parent)

        self.services = services

        # ---------------------------------------------
        # Services
        # ---------------------------------------------

        self.download_manager = services.resolve(
            ServiceNames.DOWNLOADS
        )

        # ---------------------------------------------
        # Window
        # ---------------------------------------------

        self.setWindowTitle(
            "Download Manager"
        )

        self.resize(
            900,
            600,
        )

        self.setModal(
            False
        )

        # ---------------------------------------------
        # UI
        # ---------------------------------------------

        self._create_widgets()

        self._build_ui()

    # =================================================
    # Widgets
    # =================================================

    def _create_widgets(self) -> None:

        self.title_label = QLabel(
            "Downloads"
        )

        self.count_label = QLabel()

        self.downloads_widget = DownloadsWidget(
            self.download_manager,
            self,
        )

        self.close_button = QPushButton(
            "Close"
        )

        self.close_button.clicked.connect(
            self.close
        )

        self._update_count()

        # ---------------------------------------------
        # Download signals
        # ---------------------------------------------

        self.download_manager.download_added.connect(
            self._update_count
        )

        self.download_manager.download_updated.connect(
            self._update_count
        )

        self.download_manager.download_finished.connect(
            self._update_count
        )

        self.download_manager.download_failed.connect(
            self._update_count
        )

    # =================================================
    # UI
    # =================================================

    def _build_ui(self) -> None:

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        layout.setSpacing(
            8
        )

        # ---------------------------------------------
        # Header
        # ---------------------------------------------

        header_layout = QHBoxLayout()

        header_layout.addWidget(
            self.title_label
        )

        header_layout.addWidget(
            self.count_label
        )

        header_layout.addStretch()

        header_layout.addWidget(
            self.close_button
        )

        layout.addLayout(
            header_layout
        )

        # ---------------------------------------------
        # Downloads
        # ---------------------------------------------

        layout.addWidget(
            self.downloads_widget,
            1,
        )

    # =================================================
    # Count
    # =================================================

    def _update_count(
        self,
        *_,
    ) -> None:

        count = len(
            self.download_manager.downloads()
        )

        active_count = (
            self.download_manager.active_download_count()
        )

        if count == 0:

            text = "No downloads"

        elif active_count == 0:

            text = f"{count} downloads"

        else:

            text = (
                f"{count} downloads  •  "
                f"{active_count} active"
            )

        self.count_label.setText(
            text
        )

    # =================================================
    # Close
    # =================================================

    def closeEvent(
        self,
        event,
    ) -> None:

        event.accept()