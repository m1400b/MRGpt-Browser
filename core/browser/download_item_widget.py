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

    QWidget,

    QLabel,

    QPushButton,

    QProgressBar,

    QVBoxLayout,

    QHBoxLayout,

    QSizePolicy,

)

from core.browser.download_manager import (
    DownloadItem,
    DownloadManager,
    DownloadState,
)


class DownloadItemWidget(QWidget):

    """
    نمایش یک دانلود
    """

    cancel_requested = Signal(object)

    remove_requested = Signal(object)

    open_requested = Signal(object)

    folder_requested = Signal(object)

    # ---------------------------------------------------------

    def __init__(

        self,

        item: DownloadItem,

        manager: DownloadManager,

        parent=None

    ):

        super().__init__(parent)

        self.item = item

        self.manager = manager

        self._build_ui()

        self._connect_signals()

        self.update_item(item)

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self):

        self.file_name = QLabel()

        self.file_name.setTextInteractionFlags(

            Qt.TextSelectableByMouse

        )

        self.file_name.setSizePolicy(

            QSizePolicy.Expanding,

            QSizePolicy.Preferred

        )

        # --------------------------------------------

        self.status_label = QLabel()

        self.speed_label = QLabel()

        self.progress = QProgressBar()

        self.progress.setMinimum(0)

        self.progress.setMaximum(100)

        self.progress.setTextVisible(True)

        # --------------------------------------------

        self.open_button = QPushButton("Open")

        self.folder_button = QPushButton("Folder")

        self.cancel_button = QPushButton("Cancel")

        self.remove_button = QPushButton("Remove")

        # --------------------------------------------

        title_layout = QHBoxLayout()

        title_layout.addWidget(

            self.file_name

        )

        title_layout.addStretch()

        # --------------------------------------------

        info_layout = QHBoxLayout()

        info_layout.addWidget(

            self.status_label

        )

        info_layout.addStretch()

        info_layout.addWidget(

            self.speed_label

        )

        # --------------------------------------------

        button_layout = QHBoxLayout()

        button_layout.addWidget(

            self.open_button

        )

        button_layout.addWidget(

            self.folder_button

        )

        button_layout.addWidget(

            self.cancel_button

        )

        button_layout.addWidget(

            self.remove_button

        )

        # --------------------------------------------

        layout = QVBoxLayout(self)

        layout.setContentsMargins(

            10,

            8,

            10,

            8

        )

        layout.setSpacing(6)

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
    
        # =========================================================
    # Signals
    # =========================================================

    def _connect_signals(self):

        self.open_button.clicked.connect(

            lambda:

            self.open_requested.emit(
                self.item
            )

        )

        self.folder_button.clicked.connect(

            lambda:

            self.folder_requested.emit(
                self.item
            )

        )

        self.cancel_button.clicked.connect(

            lambda:

            self.cancel_requested.emit(
                self.item
            )

        )

        self.remove_button.clicked.connect(

            lambda:

            self.remove_requested.emit(
                self.item
            )

        )

    # =========================================================
    # Update
    # =========================================================

    def update_item(
        self,
        item: DownloadItem
    ):

        self.item = item

        self.file_name.setText(
            item.filename
        )

        self.progress.setValue(
            item.progress
        )

        #
        # Status
        #

        if item.total_bytes > 0:

            status = (

                f"{DownloadManager.format_size(item.received_bytes)}"

                " / "

                f"{DownloadManager.format_size(item.total_bytes)}"

            )

        else:

            status = DownloadManager.format_size(

                item.received_bytes

            )

        self.status_label.setText(
            status
        )

        #
        # Speed + ETA
        #

        speed = DownloadManager.format_speed(
            item.speed
        )

        eta = DownloadManager.format_eta(
            item.eta
        )

        self.speed_label.setText(

            f"{speed}   {eta}"

        )

        self._update_buttons()

    # =========================================================
    # Buttons
    # =========================================================

    def _update_buttons(self):

        state = self.item.state

        #
        # Open
        #

        finished = (

            state == "finished"

        )

        downloading = (

            state == "downloading"

        )

        self.open_button.setEnabled(

            finished

        )

        self.folder_button.setEnabled(

            finished

        )

        self.cancel_button.setEnabled(

            downloading

        )

        self.remove_button.setEnabled(

            not downloading

        )

        #
        # Tooltip
        #

        self.cancel_button.setToolTip(

            "Cancel download"

        )

        self.open_button.setToolTip(

            "Open file"

        )

        self.folder_button.setToolTip(

            "Open containing folder"

        )

        self.remove_button.setToolTip(

            "Remove from history"

        )
    
        # =========================================================
    # Refresh
    # =========================================================

    def refresh(self):

        self.update_item(
            self.item
        )

    # =========================================================
    # Appearance
    # =========================================================

    def _update_state_style(self):

        state = self.item.state

        if state == DownloadState.Downloading.value:

            self.status_label.setStyleSheet(

                "color:#1565C0;font-weight:bold;"

            )

            self.progress.setFormat(

                "%p%"

            )

        elif state == DownloadState.Finished.value:

            self.status_label.setStyleSheet(

                "color:#2E7D32;font-weight:bold;"

            )

            self.progress.setValue(100)

            self.progress.setFormat(

                "Completed"

            )

        elif state == DownloadState.Cancelled.value:

            self.status_label.setStyleSheet(

                "color:#EF6C00;font-weight:bold;"

            )

            self.progress.setFormat(

                "Cancelled"

            )

        elif state == DownloadState.Interrupted.value:

            self.status_label.setStyleSheet(

                "color:#C62828;font-weight:bold;"

            )

            self.progress.setFormat(

                "Interrupted"

            )

        elif state == DownloadState.Failed.value:

            self.status_label.setStyleSheet(

                "color:#B71C1C;font-weight:bold;"

            )

            self.progress.setFormat(

                "Failed"

            )

        else:

            self.status_label.setStyleSheet("")

            self.progress.setFormat(

                "%p%"

            )

    # =========================================================
    # File Icon
    # =========================================================

    def _update_icon(self):

        path = Path(
            self.item.path
        )

        icon = QIcon.fromTheme(

            "text-x-generic"

        )

        if path.exists():

            from PySide6.QtWidgets import QFileIconProvider

            provider = QFileIconProvider()

            icon = provider.icon(path)

        self.file_name.setPixmap(
            icon.pixmap(20, 20)
        )

    # =========================================================
    # Public
    # =========================================================

    def set_item(
        self,
        item: DownloadItem
    ):

        self.item = item

        self.update_item(
            item
        )

        self._update_state_style()

        self._update_icon()

    # =========================================================
    # QWidget
    # =========================================================

    def sizeHint(self):

        return self.minimumSizeHint()

    def minimumSizeHint(self):

        return self.layout().sizeHint()