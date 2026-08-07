"""
MRGpt Browser

Downloads Panel
"""

from __future__ import annotations

from PySide6.QtCore import (
    Qt,
)

from core.browser.download_manager import (
    DownloadManager,
    DownloadItem,
    DownloadState,
)


from PySide6.QtWidgets import (

    QWidget,

    QLabel,

    QPushButton,

    QVBoxLayout,

    QHBoxLayout,

    QScrollArea,

    QFrame,

)

from core.browser.download_manager import (
    DownloadManager,
    DownloadItem,
)

from core.browser.download_item_widget import (
    DownloadItemWidget,
)


class DownloadsPanel(QWidget):

    """
    Download Manager Panel
    """

    # ------------------------------------------------------

    def __init__(

        self,

        manager: DownloadManager,

        parent=None

    ):

        super().__init__(parent)

        self.manager = manager

        self.items = {}

        self._build_ui()

        self._connect_signals()

        self.load_history()

    # ======================================================
    # UI
    # ======================================================

    def _build_ui(self):

        #
        # Header
        #

        self.title_label = QLabel(

            "Downloads"

        )

        self.title_label.setStyleSheet(

            """

            font-size:14pt;

            font-weight:bold;

            """

        )

        self.clear_button = QPushButton(

            "Clear Finished"

        )

        # ----------------------------------------------

        header_layout = QHBoxLayout()

        header_layout.addWidget(

            self.title_label

        )

        header_layout.addStretch()

        header_layout.addWidget(

            self.clear_button

        )

        # ----------------------------------------------

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

            8

        )

        # ----------------------------------------------

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

        # ----------------------------------------------

        layout = QVBoxLayout(self)

        layout.setContentsMargins(

            0,

            0,

            0,

            0

        )

        layout.setSpacing(0)

        layout.addLayout(

            header_layout

        )

        layout.addWidget(

            self.scroll

        )

        self.setMinimumWidth(

            420

        )

        self.setMinimumHeight(

            500

        )
        
        # ======================================================
    # Signals
    # ======================================================

    def _connect_signals(self):

        self.clear_button.clicked.connect(

            self.clear_finished

        )

        self.manager.download_added.connect(

            self.add_download

        )

        self.manager.download_progress.connect(

            self.update_download

        )

        self.manager.download_finished.connect(

            self.update_download

        )

        self.manager.download_failed.connect(

            self.update_download

        )

        self.manager.download_removed.connect(

            self.remove_download

        )

    # ======================================================
    # History
    # ======================================================

    def load_history(self):

        for item in self.manager.history_items():

            self.add_download(
                item
            )

    # ======================================================
    # Add Download
    # ======================================================

    def add_download(

        self,

        item: DownloadItem

    ):

        #
        # قبلاً اضافه شده
        #

        if item.id in self.items:

            return

        widget = DownloadItemWidget(

            item,

            self.manager,

            self

        )

        #
        # Signals
        #

        widget.cancel_requested.connect(

            self.manager.cancel

        )

        widget.open_requested.connect(

            self.manager.open_file

        )

        widget.folder_requested.connect(

            self.manager.open_folder

        )

        widget.remove_requested.connect(

            self.manager.remove_download

        )

        self.items[
            item.id
        ] = widget

        self.container_layout.insertWidget(

            0,

            widget

        )
        
        self.update_title()

        self._update_empty_state()

    # ======================================================
    # Update
    # ======================================================

    def update_download(

        self,

        item: DownloadItem

    ):

        widget = self.items.get(

            item.id

        )

        if widget is None:

            return

        widget.set_item(
            item
        )

    # ======================================================
    # Remove
    # ======================================================

    def remove_download(

        self,

        item: DownloadItem

    ):

        widget = self.items.pop(

            item.id,

            None

        )

        if widget is None:

            return

        self.container_layout.removeWidget(

            widget

        )
        self.manager.remove_download(item)
        widget.deleteLater()
        
        self.update_title()

        self._update_empty_state()

    # ======================================================
    # Clear Finished
    # ======================================================

    def clear_finished(self):

        self.manager.clear_finished()

        for item_id in list(

            self.items.keys()

        ):

            widget = self.items[item_id]

            if (

                widget.item.state

                ==

                "finished"

            ):

                self.remove_download(

                    widget.item

                )
        self.update_title()

        self._update_empty_state()
    
        # ======================================================
    # Empty State
    # ======================================================

    def _update_empty_state(self):

        has_items = bool(self.items)

        if has_items:

            if hasattr(self, "_empty_label"):

                self._empty_label.hide()

        else:

            if not hasattr(self, "_empty_label"):

                self._empty_label = QLabel(

                    "No downloads"

                )

                self._empty_label.setAlignment(

                    Qt.AlignCenter

                )

                self._empty_label.setStyleSheet(

                    """

                    color:gray;

                    font-size:12pt;

                    padding:40px;

                    """

                )

                self.container_layout.addWidget(

                    self._empty_label

                )

            self._empty_label.show()

    # ======================================================
    # Statistics
    # ======================================================

    def update_title(self):

        total = len(self.items)

        active = sum(

            1

            for widget in self.items.values()

            if widget.item.state == DownloadState.Downloading.value

        )

        self.title_label.setText(

            f"Downloads ({total})"

        )

        self.clear_button.setEnabled(

            total > 0

        )

    # ======================================================
    # Refresh
    # ======================================================

    def refresh(self):

        self.update_title()

        self._update_empty_state()

        for widget in self.items.values():

            widget.refresh()

    # ======================================================
    # QWidget
    # ======================================================

    def showEvent(self, event):

        super().showEvent(event)

        self.refresh()

    # ======================================================
    # Public API
    # ======================================================

    def manager_instance(self):

        return self.manager