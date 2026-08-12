"""
MRGpt Browser

Download Manager
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest

from models.download_item import DownloadItem


class DownloadManager(QObject):
    """
    Manage browser downloads.

    Responsibilities
    ----------------
    - Accept QWebEngine download requests
    - Create DownloadItem models
    - Configure download destination
    - Track progress
    - Handle completion
    - Handle cancellation
    """

    # -------------------------------------------------
    # Signals
    # -------------------------------------------------

    download_added = Signal(object)

    download_updated = Signal(object)

    download_finished = Signal(object)

    download_failed = Signal(object)

    # -------------------------------------------------

    def __init__(
        self,
        settings,
        parent=None,
    ) -> None:

        super().__init__(parent)

        self.settings = settings

        self._downloads: list[DownloadItem] = []

        # Requests that have already been accepted.
        self._accepted_requests: set[int] = set()

    # =================================================
    # Public API
    # =================================================

    def downloads(self) -> list[DownloadItem]:

        return list(
            self._downloads
        )

    # =================================================
    # Download
    # =================================================

    def handle_download(
        self,
        request: QWebEngineDownloadRequest,
    ) -> None:

        if request is None:

            return

        # -------------------------------------------------
        # Prevent duplicate processing
        # -------------------------------------------------

        request_id = id(request)

        if request_id in self._accepted_requests:

            print(
                "⚠️ DOWNLOAD REQUEST ALREADY ACCEPTED"
            )

            return

        self._accepted_requests.add(
            request_id
        )

        print(
            "🔥 DOWNLOAD MANAGER RECEIVED:"
        )

        print(
            "URL:",
            request.url().toString(),
        )

        filename = request.downloadFileName()

        print(
            "FILE:",
            filename,
        )

        # -------------------------------------------------
        # Read download directory from Settings
        # -------------------------------------------------

        directory = self.settings.download_path

        if not directory:

            directory = str(
                Path.home() / "Downloads"
            )

        directory = Path(
            directory
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        # -------------------------------------------------
        # Create DownloadItem
        # -------------------------------------------------

        item = DownloadItem(

            filename=filename,

            url=request.url().toString(),

            directory=str(directory),

            mime_type=request.mimeType(),

            total_bytes=request.totalBytes(),

            _request=request,

        )

        item.state = "downloading"

        # -------------------------------------------------
        # Store
        # -------------------------------------------------

        self._downloads.append(
            item
        )

        self.download_added.emit(
            item
        )

        # -------------------------------------------------
        # Configure request
        #
        # MUST happen before accept()
        # -------------------------------------------------

        request.setDownloadDirectory(
            str(directory)
        )

        request.setDownloadFileName(
            filename
        )

        # -------------------------------------------------
        # Signals
        # -------------------------------------------------

        request.receivedBytesChanged.connect(

            lambda:
            self._update_progress(
                item
            )

        )

        request.stateChanged.connect(

            lambda state:
            self._state_changed(
                item,
                state,
            )

        )

        # -------------------------------------------------
        # Accept
        # -------------------------------------------------

        request.accept()

        print(
            "✅ DOWNLOAD ACCEPTED"
        )

        print(
            "PATH:",
            item.full_path,
        )

    # =================================================
    # Progress
    # =================================================

    def _update_progress(
        self,
        item: DownloadItem,
    ) -> None:

        request = item._request

        if request is None:

            return

        received = request.receivedBytes()

        total = request.totalBytes()

        item.update_progress(
            received,
            total,
        )

        self.download_updated.emit(
            item
        )

    # =================================================
    # State
    # =================================================

    def _state_changed(
        self,
        item: DownloadItem,
        state,
    ) -> None:

        if state == (
            QWebEngineDownloadRequest.DownloadCompleted
        ):

            self._finish(
                item
            )

            return

        if state == (
            QWebEngineDownloadRequest.DownloadCancelled
        ):

            item.cancel()

            self.download_updated.emit(
                item
            )

            self.download_finished.emit(
                item
            )

            return

        if state == (
            QWebEngineDownloadRequest.DownloadInterrupted
        ):

            item.interrupt()

            self.download_updated.emit(
                item
            )

            self.download_failed.emit(
                item
            )

            return

    # =================================================
    # Finish
    # =================================================

    def _finish(
        self,
        item: DownloadItem,
    ) -> None:

        item.finish()

        item.progress = 100.0

        self.download_updated.emit(
            item
        )

        self.download_finished.emit(
            item
        )

    # =================================================
    # Controls
    # =================================================

    def cancel(
        self,
        item: DownloadItem,
    ) -> None:

        request = item._request

        if request is None:

            return

        request.cancel()

    # -------------------------------------------------

    def pause(
        self,
        item: DownloadItem,
    ) -> None:

        request = item._request

        if request is None:

            return

        request.pause()

        item.pause()

        self.download_updated.emit(
            item
        )

    # -------------------------------------------------

    def resume(
        self,
        item: DownloadItem,
    ) -> None:

        request = item._request

        if request is None:

            return

        request.resume()

        item.resume()

        self.download_updated.emit(
            item
        )