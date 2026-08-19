"""
MRGpt Browser

Download Item Widget
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import (
    Qt,
    Signal,
)

from PySide6.QtGui import (
    QIcon,
)

from PySide6.QtWidgets import (
    QFileIconProvider,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from models.download_item import DownloadItem

from services.download_manager import (
    DownloadManager,
)


class DownloadItemWidget(QWidget):
    """
    Visual representation of a single DownloadItem.

    Supported actions
    -----------------
    - Pause
    - Resume
    - Cancel
    - Open file
    - Open containing folder
    - Remove from download history

    State model
    -----------
    waiting
    downloading
    paused
    completed
    canceled
    interrupted
    failed
    """

    # =========================================================
    # Signals
    # =========================================================

    pause_requested = Signal(object)

    resume_requested = Signal(object)

    cancel_requested = Signal(object)

    remove_requested = Signal(object)

    open_requested = Signal(object)

    folder_requested = Signal(object)

    # =========================================================
    # Constructor
    # =========================================================

    def __init__(
        self,
        item: DownloadItem,
        manager: DownloadManager,
        parent=None,
    ) -> None:

        super().__init__(
            parent
        )

        self.item = item

        self.manager = manager

        self._build_ui()

        self._connect_signals()

        self.update_item(
            item
        )

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(
        self,
    ) -> None:

        # -----------------------------------------------------
        # File name
        # -----------------------------------------------------

        self.file_name = QLabel()

        self.file_name.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        self.file_name.setWordWrap(
            True
        )

        self.file_name.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred,
        )

        # -----------------------------------------------------
        # Status
        # -----------------------------------------------------

        self.status_label = QLabel()

        self.speed_label = QLabel()

        # -----------------------------------------------------
        # Progress
        # -----------------------------------------------------

        self.progress = QProgressBar()

        self.progress.setMinimum(
            0
        )

        self.progress.setMaximum(
            100
        )

        self.progress.setTextVisible(
            True
        )

        self.progress.setFormat(
            "%p%"
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        self.open_button = QPushButton(
            "Open"
        )

        self.folder_button = QPushButton(
            "Folder"
        )

        self.pause_button = QPushButton(
            "Pause"
        )

        self.resume_button = QPushButton(
            "Resume"
        )

        self.cancel_button = QPushButton(
            "Cancel"
        )

        self.remove_button = QPushButton(
            "Remove"
        )

        # -----------------------------------------------------
        # Title
        # -----------------------------------------------------

        title_layout = QHBoxLayout()

        title_layout.addWidget(
            self.file_name
        )

        title_layout.addStretch()

        # -----------------------------------------------------
        # Information
        # -----------------------------------------------------

        info_layout = QHBoxLayout()

        info_layout.addWidget(
            self.status_label
        )

        info_layout.addStretch()

        info_layout.addWidget(
            self.speed_label
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.open_button
        )

        button_layout.addWidget(
            self.folder_button
        )

        button_layout.addWidget(
            self.pause_button
        )

        button_layout.addWidget(
            self.resume_button
        )

        button_layout.addWidget(
            self.cancel_button
        )

        button_layout.addWidget(
            self.remove_button
        )

        # -----------------------------------------------------
        # Main layout
        # -----------------------------------------------------

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            10,
            8,
            10,
            8,
        )

        layout.setSpacing(
            6
        )

        layout.addLayout(
            title_layout
        )

        layout.addWidget(
            self.progress
        )

        layout.addLayout(
            info_layout
        )

        layout.addLayout(
            button_layout
        )

        # -----------------------------------------------------
        # Appearance
        # -----------------------------------------------------

        self.setStyleSheet(
            """
            DownloadItemWidget {
                border: 1px solid #d9d9d9;
                border-radius: 8px;
                background: palette(base);
            }
            """
        )

    # =========================================================
    # Signals
    # =========================================================

    def _connect_signals(
        self,
    ) -> None:

        self.pause_button.clicked.connect(
            self._on_pause
        )

        self.resume_button.clicked.connect(
            self._on_resume
        )

        self.cancel_button.clicked.connect(
            self._on_cancel
        )

        self.remove_button.clicked.connect(
            self._on_remove
        )

        self.open_button.clicked.connect(
            self._on_open
        )

        self.folder_button.clicked.connect(
            self._on_folder
        )

    # =========================================================
    # Actions
    # =========================================================

    def _on_pause(
        self,
    ) -> None:

        self.pause_requested.emit(
            self.item
        )

    # ---------------------------------------------------------

    def _on_resume(
        self,
    ) -> None:

        self.resume_requested.emit(
            self.item
        )

    # ---------------------------------------------------------

    def _on_cancel(
        self,
    ) -> None:

        self.cancel_requested.emit(
            self.item
        )

    # ---------------------------------------------------------

    def _on_remove(
        self,
    ) -> None:

        self.remove_requested.emit(
            self.item
        )

    # ---------------------------------------------------------

    def _on_open(
        self,
    ) -> None:

        self.open_requested.emit(
            self.item
        )

    # ---------------------------------------------------------

    def _on_folder(
        self,
    ) -> None:

        self.folder_requested.emit(
            self.item
        )

    # =========================================================
    # Update
    # =========================================================

    def update_item(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Refresh the widget from DownloadItem.
        """

        self.item = item

        # -----------------------------------------------------
        # Filename
        # -----------------------------------------------------

        self.file_name.setText(
            item.filename
        )

        # -----------------------------------------------------
        # Progress
        # -----------------------------------------------------

        progress = int(
            max(
                0.0,
                min(
                    100.0,
                    item.progress,
                ),
            )
        )

        self.progress.setValue(
            progress
        )

        # -----------------------------------------------------
        # Size
        # -----------------------------------------------------

        received = self._format_bytes(
            item.received_bytes
        )

        if item.total_bytes > 0:

            total = self._format_bytes(
                item.total_bytes
            )

            status = (
                f"{received} / {total}"
            )

        else:

            status = received

        self.status_label.setText(
            status
        )

        # -----------------------------------------------------
        # Speed
        # -----------------------------------------------------

        if item.speed > 0:

            speed = (
                f"{self._format_bytes(item.speed)}/s"
            )

        else:

            speed = ""

        # -----------------------------------------------------
        # ETA
        # -----------------------------------------------------

        eta = self._format_eta(
            item.remaining_seconds
        )

        if speed and eta:

            self.speed_label.setText(
                f"{speed}   {eta}"
            )

        elif speed:

            self.speed_label.setText(
                speed
            )

        elif eta:

            self.speed_label.setText(
                eta
            )

        else:

            self.speed_label.setText(
                ""
            )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        self._update_buttons()

        # -----------------------------------------------------
        # State appearance
        # -----------------------------------------------------

        self._update_state_style()

        # -----------------------------------------------------
        # File icon
        # -----------------------------------------------------

        self._update_icon()

    # =========================================================
    # Formatting
    # =========================================================

    @staticmethod
    def _format_bytes(
        value: float | int,
    ) -> str:

        value = max(
            0,
            float(value),
        )

        if value < 1024:

            return f"{int(value)} B"

        if value < 1024 ** 2:

            return (
                f"{value / 1024:.1f} KB"
            )

        if value < 1024 ** 3:

            return (
                f"{value / (1024 ** 2):.1f} MB"
            )

        return (
            f"{value / (1024 ** 3):.2f} GB"
        )

    # ---------------------------------------------------------

    @staticmethod
    def _format_eta(
        seconds: int,
    ) -> str:

        if seconds is None:

            return ""

        if seconds < 0:

            return ""

        seconds = int(
            seconds
        )

        hours, remainder = divmod(
            seconds,
            3600,
        )

        minutes, seconds = divmod(
            remainder,
            60,
        )

        if hours > 0:

            return (
                f"ETA: "
                f"{hours:02d}:"
                f"{minutes:02d}:"
                f"{seconds:02d}"
            )

        if minutes > 0:

            return (
                f"ETA: "
                f"{minutes:02d}:"
                f"{seconds:02d}"
            )

        return (
            f"ETA: "
            f"{seconds}s"
        )

    # =========================================================
    # Button State
    # =========================================================

    def _update_buttons(
        self,
    ) -> None:

        state = self.item.state

        # -----------------------------------------------------
        # State groups
        # -----------------------------------------------------

        waiting = (
            state == "waiting"
        )

        downloading = (
            state == "downloading"
        )

        paused = (
            state == "paused"
        )

        completed = (
            state == "completed"
        )

        # -----------------------------------------------------
        # File existence
        # -----------------------------------------------------

        file_exists = Path(
            self.item.full_path
        ).exists()

        # -----------------------------------------------------
        # Open
        # -----------------------------------------------------

        self.open_button.setEnabled(
            completed
            and file_exists
        )

        # -----------------------------------------------------
        # Folder
        # -----------------------------------------------------

        self.folder_button.setEnabled(
            bool(
                self.item.directory
            )
        )

        # -----------------------------------------------------
        # Pause
        # -----------------------------------------------------

        self.pause_button.setVisible(
            waiting
            or downloading
        )

        self.pause_button.setEnabled(
            waiting
            or downloading
        )

        # -----------------------------------------------------
        # Resume
        # -----------------------------------------------------

        self.resume_button.setVisible(
            paused
        )

        self.resume_button.setEnabled(
            paused
        )

        # -----------------------------------------------------
        # Cancel
        # -----------------------------------------------------

        self.cancel_button.setEnabled(
            waiting
            or downloading
            or paused
        )

        # -----------------------------------------------------
        # Remove
        # -----------------------------------------------------

        self.remove_button.setEnabled(
            not (
                waiting
                or downloading
                or paused
            )
        )

        # -----------------------------------------------------
        # Tooltips
        # -----------------------------------------------------

        self.pause_button.setToolTip(
            "Pause download"
        )

        self.resume_button.setToolTip(
            "Resume download"
        )

        self.cancel_button.setToolTip(
            "Cancel download"
        )

        self.open_button.setToolTip(
            "Open downloaded file"
        )

        self.folder_button.setToolTip(
            "Open containing folder"
        )

        self.remove_button.setToolTip(
            "Remove from download history"
        )

    # =========================================================
    # State Appearance
    # =========================================================

    def _update_state_style(
        self,
    ) -> None:

        state = self.item.state

        # -----------------------------------------------------
        # Waiting
        # -----------------------------------------------------

        if state == "waiting":

            self.status_label.setStyleSheet(
                "color:#757575;font-weight:bold;"
            )

            self.progress.setFormat(
                "Waiting - %p%"
            )

        # -----------------------------------------------------
        # Downloading
        # -----------------------------------------------------

        elif state == "downloading":

            self.status_label.setStyleSheet(
                "color:#1565C0;font-weight:bold;"
            )

            self.progress.setFormat(
                "%p%"
            )

        # -----------------------------------------------------
        # Paused
        # -----------------------------------------------------

        elif state == "paused":

            self.status_label.setStyleSheet(
                "color:#EF6C00;font-weight:bold;"
            )

            self.progress.setFormat(
                "Paused - %p%"
            )

        # -----------------------------------------------------
        # Completed
        # -----------------------------------------------------

        elif state == "completed":

            self.status_label.setStyleSheet(
                "color:#2E7D32;font-weight:bold;"
            )

            self.progress.setValue(
                100
            )

            self.progress.setFormat(
                "Completed"
            )

        # -----------------------------------------------------
        # Canceled
        # -----------------------------------------------------

        elif state == "canceled":

            self.status_label.setStyleSheet(
                "color:#EF6C00;font-weight:bold;"
            )

            self.progress.setFormat(
                "Canceled"
            )

        # -----------------------------------------------------
        # Interrupted
        # -----------------------------------------------------

        elif state == "interrupted":

            self.status_label.setStyleSheet(
                "color:#C62828;font-weight:bold;"
            )

            self.progress.setFormat(
                "Interrupted"
            )

        # -----------------------------------------------------
        # Failed
        # -----------------------------------------------------

        elif state == "failed":

            self.status_label.setStyleSheet(
                "color:#B71C1C;font-weight:bold;"
            )

            self.progress.setFormat(
                "Failed"
            )

        # -----------------------------------------------------
        # Unknown
        # -----------------------------------------------------

        else:

            self.status_label.setStyleSheet(
                ""
            )

            self.progress.setFormat(
                "%p%"
            )

    # =========================================================
    # File Icon
    # =========================================================

    def _update_icon(
        self,
    ) -> None:

        path = Path(
            self.item.full_path
        )

        icon = QIcon.fromTheme(
            "text-x-generic"
        )

        if path.exists():

            try:

                provider = QFileIconProvider()

                icon = provider.icon(
                    path
                )

            except Exception:

                pass

        self.file_name.setPixmap(
            icon.pixmap(
                20,
                20,
            )
        )

    # =========================================================
    # Public API
    # =========================================================

    def set_item(
        self,
        item: DownloadItem,
    ) -> None:

        self.update_item(
            item
        )

    # ---------------------------------------------------------

    def refresh(
        self,
    ) -> None:

        self.update_item(
            self.item
        )

    # =========================================================
    # QWidget
    # =========================================================

    def sizeHint(
        self,
    ):

        return self.minimumSizeHint()

    # ---------------------------------------------------------

    def minimumSizeHint(
        self,
    ):

        return self.layout().sizeHint()