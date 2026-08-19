"""
MRGpt Browser

Downloads Panel
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import (
    Qt,
    QUrl,
)
from PySide6.QtGui import (
    QDesktopServices,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from models.download_item import DownloadItem

from services.download_manager import (
    DownloadManager,
)

from core.browser.download_item_widget import (
    DownloadItemWidget,
)


class DownloadsPanel(QWidget):
    """
    Visual panel for displaying browser downloads.

    Responsibilities
    ----------------
    - Display downloads managed by DownloadManager
    - Restore persisted download history
    - Add newly created downloads
    - Synchronize widgets with DownloadManager
    - Open completed files
    - Open containing folders
    - Remove widgets from the visual list
    """

    # =========================================================
    # Constructor
    # =========================================================

    def __init__(
        self,
        manager: DownloadManager,
        parent=None,
    ) -> None:

        super().__init__(
            parent
        )

        self.manager = manager

        # -----------------------------------------------------
        # Download widgets
        #
        # key:
        #     DownloadItem.id
        #
        # value:
        #     DownloadItemWidget
        # -----------------------------------------------------

        self.items: dict[
            int,
            DownloadItemWidget,
        ] = {}

        self._build_ui()

        self._connect_signals()

        self.load_history()

        self._update_title()

        self._update_empty_state()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(
        self,
    ) -> None:
        """
        Build the downloads panel.
        """

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        self.title_label = QLabel(
            "Downloads"
        )

        self.title_label.setStyleSheet(
            """
            font-size: 14pt;
            font-weight: bold;
            """
        )

        header_layout = QHBoxLayout()

        header_layout.setContentsMargins(
            8,
            8,
            8,
            8,
        )

        header_layout.addWidget(
            self.title_label
        )

        header_layout.addStretch()

        # -----------------------------------------------------
        # Container
        # -----------------------------------------------------

        self.container = QWidget()

        self.container_layout = QVBoxLayout(
            self.container
        )

        self.container_layout.setAlignment(
            Qt.AlignTop
        )

        self.container_layout.setSpacing(
            8
        )

        self.container_layout.setContentsMargins(
            8,
            8,
            8,
            8,
        )

        # -----------------------------------------------------
        # Empty state
        # -----------------------------------------------------

        self._empty_label = QLabel(
            "No downloads"
        )

        self._empty_label.setAlignment(
            Qt.AlignCenter
        )

        self._empty_label.setStyleSheet(
            """
            color: gray;
            font-size: 12pt;
            padding: 40px;
            """
        )

        self.container_layout.addWidget(
            self._empty_label
        )

        # -----------------------------------------------------
        # Scroll area
        # -----------------------------------------------------

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QFrame.NoFrame
        )

        self.scroll.setWidget(
            self.container
        )

        # -----------------------------------------------------
        # Main layout
        # -----------------------------------------------------

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            0
        )

        layout.addLayout(
            header_layout
        )

        layout.addWidget(
            self.scroll
        )

        # -----------------------------------------------------
        # Size
        # -----------------------------------------------------

        self.setMinimumWidth(
            420
        )

        self.setMinimumHeight(
            500
        )

    # =========================================================
    # Signals
    # =========================================================

    def _connect_signals(
        self,
    ) -> None:
        """
        Connect DownloadManager signals.
        """

        self.manager.download_added.connect(
            self.add_download
        )

        self.manager.download_updated.connect(
            self.update_download
        )

        self.manager.download_finished.connect(
            self.update_download
        )

        self.manager.download_failed.connect(
            self.update_download
        )

    # =========================================================
    # History
    # =========================================================

    def load_history(
        self,
    ) -> None:
        """
        Load persisted downloads from DownloadManager.
        """

        for item in self.manager.downloads():

            self.add_download(
                item
            )

    # =========================================================
    # Add Download
    # =========================================================

    def add_download(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Add a DownloadItem to the panel.
        """

        if item is None:

            return

        # -----------------------------------------------------
        # Already exists
        # -----------------------------------------------------

        if item.id in self.items:

            self.update_download(
                item
            )

            return

        # -----------------------------------------------------
        # Create widget
        # -----------------------------------------------------

        widget = DownloadItemWidget(
            item,
            self.manager,
            self,
        )

        # -----------------------------------------------------
        # Widget signals
        # -----------------------------------------------------

        widget.cancel_requested.connect(
            self._cancel_download
        )

        widget.remove_requested.connect(
            self._remove_download
        )

        widget.open_requested.connect(
            self._open_download
        )

        widget.folder_requested.connect(
            self._open_folder
        )

        # -----------------------------------------------------
        # Store
        # -----------------------------------------------------

        self.items[
            item.id
        ] = widget

        # -----------------------------------------------------
        # Insert at top
        # -----------------------------------------------------

        self.container_layout.insertWidget(
            0,
            widget,
        )

        # -----------------------------------------------------
        # Empty state
        # -----------------------------------------------------

        self._update_empty_state()

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        self._update_title()

    # =========================================================
    # Update
    # =========================================================

    def update_download(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Update corresponding DownloadItemWidget.
        """

        if item is None:

            return

        widget = self.items.get(
            item.id
        )

        # -----------------------------------------------------
        # Widget doesn't exist
        # -----------------------------------------------------

        if widget is None:

            self.add_download(
                item
            )

            return

        # -----------------------------------------------------
        # Update
        # -----------------------------------------------------

        widget.set_item(
            item
        )

        self._update_title()

        self._update_empty_state()

    # =========================================================
    # Cancel
    # =========================================================

    def _cancel_download(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Forward cancellation to DownloadManager.
        """

        if item is None:

            return

        self.manager.cancel(
            item
        )

    # =========================================================
    # Remove
    # =========================================================

    def _remove_download(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Remove only the visual widget.

        The DownloadItem and database record are intentionally
        untouched because the current repository contract does
        not expose a delete/remove method.
        """

        if item is None:

            return

        self.remove_widget(
            item.id
        )

    # =========================================================
    # Open Download
    # =========================================================

    def _open_download(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Open the downloaded file using the operating system.
        """

        if item is None:

            return

        if item.state != "completed":

            return

        path = Path(
            item.full_path
        )

        if not path.exists():

            print(
                "⚠️ DOWNLOAD FILE NOT FOUND:",
                path,
            )

            return

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(
                str(path)
            )
        )

    # =========================================================
    # Open Folder
    # =========================================================

    def _open_folder(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Open the folder containing the download.
        """

        if item is None:

            return

        directory = Path(
            item.directory
        )

        if not directory.exists():

            try:

                directory.mkdir(
                    parents=True,
                    exist_ok=True,
                )

            except OSError as exc:

                print(
                    "❌ FAILED TO CREATE DOWNLOAD DIRECTORY:",
                    exc,
                )

                return

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(
                str(directory)
            )
        )

    # =========================================================
    # Remove Widget
    # =========================================================

    def remove_widget(
        self,
        item_id: int,
    ) -> None:
        """
        Remove a widget from the visual panel.

        This does not remove the DownloadItem from the
        DownloadManager or database.
        """

        widget = self.items.pop(
            item_id,
            None,
        )

        if widget is None:

            return

        self.container_layout.removeWidget(
            widget
        )

        widget.deleteLater()

        self._update_title()

        self._update_empty_state()

    # =========================================================
    # Empty State
    # =========================================================

    def _update_empty_state(
        self,
    ) -> None:
        """
        Show or hide empty-state label.
        """

        has_items = bool(
            self.items
        )

        self._empty_label.setVisible(
            not has_items
        )

    # =========================================================
    # Title
    # =========================================================

    def _update_title(
        self,
    ) -> None:
        """
        Update title with total and active counts.
        """

        total = len(
            self.items
        )

        active = sum(
            1
            for widget in self.items.values()
            if widget.item.state == "downloading"
        )

        paused = sum(
            1
            for widget in self.items.values()
            if widget.item.state == "paused"
        )

        if active > 0:

            self.title_label.setText(
                f"Downloads ({total}) • "
                f"Active: {active}"
            )

        elif paused > 0:

            self.title_label.setText(
                f"Downloads ({total}) • "
                f"Paused: {paused}"
            )

        else:

            self.title_label.setText(
                f"Downloads ({total})"
            )

    # =========================================================
    # Refresh
    # =========================================================

    def refresh(
        self,
    ) -> None:
        """
        Refresh all widgets.
        """

        for widget in self.items.values():

            widget.refresh()

        self._update_title()

        self._update_empty_state()

    # =========================================================
    # QWidget
    # =========================================================

    def showEvent(
        self,
        event,
    ) -> None:

        super().showEvent(
            event
        )

        self.refresh()

    # =========================================================
    # Public API
    # =========================================================

    def manager_instance(
        self,
    ) -> DownloadManager:
        """
        Return associated DownloadManager.
        """

        return self.manager