"""
MRGpt Browser

Download Manager
"""

from __future__ import annotations

from pathlib import Path
from time import monotonic

from PySide6.QtCore import (
    QByteArray,
    QObject,
    QUrl,
    Signal,
)

from PySide6.QtNetwork import (
    QNetworkAccessManager,
    QNetworkReply,
    QNetworkRequest,
)

from PySide6.QtWebEngineCore import (
    QWebEngineDownloadRequest,
)

from models.download_item import DownloadItem


class DownloadManager(QObject):
    """
    Central manager for browser downloads.

    Responsibilities
    ----------------
    - Accept QWebEngine download requests
    - Create and persist DownloadItem objects
    - Track download progress
    - Calculate download speed
    - Pause / resume / cancel downloads
    - Restore download history
    - Resume interrupted downloads after restart
    - Persist download state
    - Safely handle application shutdown
    """

    # =========================================================
    # Signals
    # =========================================================

    download_added = Signal(object)

    download_updated = Signal(object)

    download_finished = Signal(object)

    download_failed = Signal(object)

    # =========================================================
    # Constructor
    # =========================================================

    def __init__(
        self,
        settings,
        repository,
        parent=None,
    ) -> None:

        super().__init__(
            parent
        )

        self.settings = settings

        self.repository = repository

        # -----------------------------------------------------
        # Download models
        # -----------------------------------------------------

        self._downloads: list[
            DownloadItem
        ] = []

        # -----------------------------------------------------
        # Active WebEngine requests
        # -----------------------------------------------------

        self._accepted_requests: set[
            int
        ] = set()

        # -----------------------------------------------------
        # Requests currently being paused
        #
        # IMPORTANT:
        # This marker is removed when:
        #
        #     Pause -> Cancelled signal
        #
        # AND also proactively before Resume.
        #
        # This prevents:
        #
        #     Pause -> Resume -> Pause
        #
        # from getting stuck.
        # -----------------------------------------------------

        self._pausing_requests: set[
            int
        ] = set()

        # -----------------------------------------------------
        # Progress timing
        #
        # item id ->
        #     (
        #         received_bytes,
        #         monotonic_time
        #     )
        # -----------------------------------------------------

        self._last_progress: dict[
            int,
            tuple[int, float],
        ] = {}

        # -----------------------------------------------------
        # Network manager
        #
        # Used for HTTP Range based resume after
        # application restart and for persisted downloads.
        # -----------------------------------------------------

        self._network_manager = QNetworkAccessManager(
            self
        )

        # -----------------------------------------------------
        # Active resume replies
        #
        # item id -> QNetworkReply
        # -----------------------------------------------------

        self._resume_replies: dict[
            int,
            QNetworkReply,
        ] = {}

        # -----------------------------------------------------
        # Resume pause markers
        #
        # Used when a resumed QNetworkReply is intentionally
        # aborted in order to pause the download.
        # -----------------------------------------------------

        self._pausing_resume_ids: set[
            int
        ] = set()

        # -----------------------------------------------------
        # Restore history
        # -----------------------------------------------------

        self._load_downloads()

    # =========================================================
    # Public API
    # =========================================================

    def downloads(
        self,
    ) -> list[DownloadItem]:
        """
        Return all known downloads.
        """

        return list(
            self._downloads
        )

    # ---------------------------------------------------------

    def active_downloads(
        self,
    ) -> list[DownloadItem]:
        """
        Return downloads that can currently be controlled.

        A paused download is considered active because it
        remains resumable.
        """

        return [
            item
            for item in self._downloads
            if item.is_active
        ]

    # ---------------------------------------------------------

    def has_active_downloads(
        self,
    ) -> bool:
        """
        Return True when at least one active download exists.
        """

        return any(
            item.is_active
            for item in self._downloads
        )

    # ---------------------------------------------------------

    def active_download_count(
        self,
    ) -> int:
        """
        Return the number of active downloads.
        """

        return sum(
            1
            for item in self._downloads
            if item.is_active
        )

    # =========================================================
    # Download Creation
    # =========================================================

    def handle_download(
        self,
        request: QWebEngineDownloadRequest,
    ) -> None:
        """
        Accept and register a new WebEngine download.
        """

        if request is None:

            return

        request_id = id(
            request
        )

        # -----------------------------------------------------
        # Prevent duplicate processing
        # -----------------------------------------------------

        if request_id in self._accepted_requests:

            print(
                "⚠️ DOWNLOAD REQUEST ALREADY ACCEPTED"
            )

            return

        self._accepted_requests.add(
            request_id
        )

        # -----------------------------------------------------
        # Basic information
        # -----------------------------------------------------

        url = request.url().toString()

        filename = request.downloadFileName()

        if not filename:

            filename = "download"

        print(
            "🔥 DOWNLOAD MANAGER RECEIVED:"
        )

        print(
            "URL:",
            url,
        )

        print(
            "FILE:",
            filename,
        )

        # -----------------------------------------------------
        # Download directory
        # -----------------------------------------------------

        directory = getattr(
            self.settings,
            "download_path",
            "",
        )

        if not directory:

            directory = str(
                Path.home()
                / "Downloads"
            )

        directory = Path(
            directory
        )

        try:

            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

        except OSError as exc:

            print(
                "❌ DOWNLOAD DIRECTORY ERROR:",
                exc,
            )

            self._accepted_requests.discard(
                request_id
            )

            return

        # -----------------------------------------------------
        # Create model
        # -----------------------------------------------------

        item = DownloadItem(

            filename=filename,

            url=url,

            directory=str(
                directory
            ),

            mime_type=request.mimeType(),

            total_bytes=max(
                0,
                request.totalBytes(),
            ),

            _request=request,
        )

        item.start()

        # -----------------------------------------------------
        # Progress timing
        # -----------------------------------------------------

        self._last_progress[
            item.id
        ] = (
            0,
            monotonic(),
        )

        # -----------------------------------------------------
        # Store in memory
        # -----------------------------------------------------

        self._downloads.append(
            item
        )

        # -----------------------------------------------------
        # Persist initial item
        # -----------------------------------------------------

        self._persist_add(
            item
        )

        # -----------------------------------------------------
        # Notify UI
        # -----------------------------------------------------

        self.download_added.emit(
            item
        )

        # -----------------------------------------------------
        # Configure destination
        #
        # MUST happen before accept().
        # -----------------------------------------------------

        request.setDownloadDirectory(
            str(directory)
        )

        request.setDownloadFileName(
            filename
        )

        # -----------------------------------------------------
        # Signals
        # -----------------------------------------------------

        request.receivedBytesChanged.connect(
            lambda: self._update_progress(
                item
            )
        )

        request.stateChanged.connect(
            lambda state: self._state_changed(
                item,
                state,
            )
        )

        # -----------------------------------------------------
        # Accept
        # -----------------------------------------------------

        try:

            request.accept()

        except Exception as exc:

            print(
                "❌ DOWNLOAD ACCEPT FAILED:",
                exc,
            )

            item.fail()

            self._persist_item(
                item
            )

            self.download_updated.emit(
                item
            )

            self.download_failed.emit(
                item
            )

            return

        print(
            "✅ DOWNLOAD ACCEPTED"
        )

        print(
            "PATH:",
            item.full_path,
        )

    # =========================================================
    # Progress
    # =========================================================

    def _update_progress(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Update progress and speed of a live WebEngine
        download.
        """

        request = item._request

        if request is None:

            return

        try:

            received = max(
                0,
                request.receivedBytes(),
            )

            total = max(
                0,
                request.totalBytes(),
            )

        except RuntimeError:

            return

        # -----------------------------------------------------
        # Speed
        # -----------------------------------------------------

        now = monotonic()

        previous = self._last_progress.get(
            item.id
        )

        if previous is not None:

            previous_bytes, previous_time = previous

            elapsed = (
                now
                - previous_time
            )

            delta = (
                received
                - previous_bytes
            )

            if (
                elapsed > 0
                and delta >= 0
            ):

                item.speed = (
                    delta
                    / elapsed
                )

        self._last_progress[
            item.id
        ] = (
            received,
            now,
        )

        # -----------------------------------------------------
        # ETA
        # -----------------------------------------------------

        if (
            item.speed > 0
            and total > received
        ):

            item.remaining_seconds = int(
                (
                    total
                    - received
                )
                / item.speed
            )

        else:

            item.remaining_seconds = -1

        # -----------------------------------------------------
        # Model
        # -----------------------------------------------------

        item.update_progress(
            received,
            total,
        )

        # -----------------------------------------------------
        # Persistence
        # -----------------------------------------------------

        self._persist_progress(
            item
        )

        # -----------------------------------------------------
        # UI
        # -----------------------------------------------------

        self.download_updated.emit(
            item
        )

    # =========================================================
    # State
    # =========================================================

    def _state_changed(
        self,
        item: DownloadItem,
        state,
    ) -> None:
        """
        Handle QWebEngineDownloadRequest state changes.
        """

        # =====================================================
        # Completed
        # =====================================================

        if state == (
            QWebEngineDownloadRequest
            .DownloadCompleted
        ):

            self._finish(
                item
            )

            return

        # =====================================================
        # Cancelled
        # =====================================================

        if state == (
            QWebEngineDownloadRequest
            .DownloadCancelled
        ):

            request = item._request

            request_id = (
                id(request)
                if request is not None
                else None
            )

            # -------------------------------------------------
            # Cancellation caused by Pause / Shutdown
            # -------------------------------------------------

            if (
                request_id is not None
                and request_id in self._pausing_requests
            ):

                self._pausing_requests.discard(
                    request_id
                )

                return

            # -------------------------------------------------
            # Real cancellation
            # -------------------------------------------------

            item.cancel()

            self._sync_file_progress(
                item
            )

            self._persist_item(
                item
            )

            self.download_updated.emit(
                item
            )

            self.download_finished.emit(
                item
            )

            return

        # =====================================================
        # Interrupted
        # =====================================================

        if state == (
            QWebEngineDownloadRequest
            .DownloadInterrupted
        ):

            item.interrupt()

            self._sync_file_progress(
                item
            )

            self._persist_item(
                item
            )

            self.download_updated.emit(
                item
            )

            self.download_failed.emit(
                item
            )

    # =========================================================
    # Finish
    # =========================================================

    def _finish(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Mark download as completed.
        """

        self._sync_file_progress(
            item
        )

        item.finish()

        item.progress = 100.0

        item.remaining_seconds = 0

        # -----------------------------------------------------
        # Persist
        # -----------------------------------------------------

        self._persist_item(
            item
        )

        # -----------------------------------------------------
        # UI
        # -----------------------------------------------------

        self.download_updated.emit(
            item
        )

        self.download_finished.emit(
            item
        )

        # -----------------------------------------------------
        # Cleanup timing
        # -----------------------------------------------------

        self._last_progress.pop(
            item.id,
            None,
        )

        # -----------------------------------------------------
        # Cleanup pause marker
        # -----------------------------------------------------

        request = item._request

        if request is not None:

            self._pausing_requests.discard(
                id(request)
            )

    # =========================================================
    # Manual Controls
    # =========================================================

    def cancel(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Cancel a download.
        """

        if item is None:

            return

        # -----------------------------------------------------
        # Cancel resumed download
        # -----------------------------------------------------

        reply = self._resume_replies.get(
            item.id
        )

        if reply is not None:

            self._pausing_resume_ids.discard(
                item.id
            )

            try:

                reply.abort()

            except Exception as exc:

                print(
                    "⚠️ FAILED TO ABORT RESUME:",
                    exc,
                )

            item.cancel()

            self._persist_item(
                item
            )

            self.download_updated.emit(
                item
            )

            self.download_finished.emit(
                item
            )

            self._cleanup_resume_reply(
                item.id,
                reply,
            )

            return

        # -----------------------------------------------------
        # WebEngine download
        # -----------------------------------------------------

        request = item._request

        if request is None:

            # -------------------------------------------------
            # Persisted item without live request.
            # -------------------------------------------------

            if item.is_active:

                item.cancel()

                self._persist_item(
                    item
                )

                self.download_updated.emit(
                    item
                )

                self.download_finished.emit(
                    item
                )

            return

        # -----------------------------------------------------
        # Cancellation is NOT a pause.
        #
        # Remove any stale pause marker first.
        # -----------------------------------------------------

        self._pausing_requests.discard(
            id(request)
        )

        try:

            request.cancel()

        except Exception as exc:

            print(
                "⚠️ DOWNLOAD CANCEL FAILED:",
                exc,
            )

    # ---------------------------------------------------------

    def cancel_all_active(
        self,
    ) -> None:
        """
        Cancel all active downloads.
        """

        for item in list(
            self.active_downloads()
        ):

            self.cancel(
                item
            )

    # =========================================================
    # Pause
    # =========================================================

    def pause(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Pause a download.

        Handles both:

        1. Live QWebEngine downloads.
        2. Downloads resumed through HTTP Range.
        """

        if item is None:

            return

        print(
            f"⏸️ PAUSE REQUESTED: {item.filename}"
        )

        # =====================================================
        # Resumed download
        # =====================================================

        reply = self._resume_replies.get(
            item.id
        )

        if reply is not None:

            if item.id in self._pausing_resume_ids:

                print(
                    f"⚠️ PAUSE ALREADY IN PROGRESS: "
                    f"{item.filename}"
                )

                return

            self._pausing_resume_ids.add(
                item.id
            )

            try:

                reply.abort()

            except Exception as exc:

                print(
                    "⚠️ FAILED TO ABORT RESUME:",
                    exc,
                )

                self._pausing_resume_ids.discard(
                    item.id
                )

            return

        # =====================================================
        # Live WebEngine download
        # =====================================================

        request = item._request

        if request is None:

            print(
                "⚠️ NO ACTIVE DOWNLOAD REQUEST"
            )

            return

        request_id = id(
            request
        )

        # -----------------------------------------------------
        # IMPORTANT
        #
        # If the user presses Pause twice before the
        # WebEngine stateChanged signal arrives, do not
        # issue multiple pause calls.
        # -----------------------------------------------------

        if request_id in self._pausing_requests:

            print(
                f"⚠️ PAUSE ALREADY IN PROGRESS: "
                f"{item.filename}"
            )

            return

        self._pausing_requests.add(
            request_id
        )

        # -----------------------------------------------------
        # Synchronize actual file size first
        # -----------------------------------------------------

        self._sync_file_progress(
            item
        )

        # -----------------------------------------------------
        # Pause
        # -----------------------------------------------------

        try:

            request.pause()

        except Exception as exc:

            print(
                "⚠️ DOWNLOAD PAUSE FAILED:",
                exc,
            )

            self._pausing_requests.discard(
                request_id
            )

            return

        # -----------------------------------------------------
        # Model
        # -----------------------------------------------------

        item.pause()

        item.speed = 0.0

        item.remaining_seconds = -1

        # -----------------------------------------------------
        # Persist
        # -----------------------------------------------------

        self._persist_item(
            item
        )

        self.download_updated.emit(
            item
        )

    # =========================================================
    # Resume
    # =========================================================

    def resume(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Resume a live WebEngine download.

        For persisted downloads without a live request,
        resume_download() is used.
        """

        if item is None:

            return

        request = item._request

        # -----------------------------------------------------
        # Persisted download
        # -----------------------------------------------------

        if request is None:

            self.resume_download(
                item.id
            )

            return

        # -----------------------------------------------------
        # Only paused downloads can be resumed.
        # -----------------------------------------------------

        if item.state != "paused":

            return

        request_id = id(
            request
        )

        # -----------------------------------------------------
        # CRITICAL FIX
        #
        # A previous Pause places request_id in
        # _pausing_requests.
        #
        # WebEngine normally removes it when DownloadCancelled
        # is emitted, but depending on timing that signal may
        # arrive before/after Resume.
        #
        # Therefore Resume explicitly clears the stale marker.
        #
        # This fixes:
        #
        #     Pause
        #     Resume
        #     Pause
        #
        # and repeated cycles thereafter.
        # -----------------------------------------------------

        self._pausing_requests.discard(
            request_id
        )

        # -----------------------------------------------------
        # Resume
        # -----------------------------------------------------

        try:

            request.resume()

        except Exception as exc:

            print(
                "⚠️ DOWNLOAD RESUME FAILED:",
                exc,
            )

            return

        # -----------------------------------------------------
        # Model
        # -----------------------------------------------------

        item.resume()

        item.speed = 0.0

        item.remaining_seconds = -1

        # -----------------------------------------------------
        # Reset progress timing
        # -----------------------------------------------------

        self._last_progress[
            item.id
        ] = (
            item.received_bytes,
            monotonic(),
        )

        # -----------------------------------------------------
        # Persist
        # -----------------------------------------------------

        self._persist_item(
            item
        )

        # -----------------------------------------------------
        # UI
        # -----------------------------------------------------

        self.download_updated.emit(
            item
        )

        print(
            f"▶️ DOWNLOAD RESUMED: "
            f"{item.filename}"
        )

    # =========================================================
    # Shutdown
    # =========================================================

    def pause_all_active(
        self,
    ) -> None:
        """
        Pause all active live WebEngine downloads before
        application shutdown.
        """

        for item in list(
            self.active_downloads()
        ):

            # -------------------------------------------------
            # Already paused
            # -------------------------------------------------

            if item.state == "paused":

                self._sync_file_progress(
                    item
                )

                self._persist_item(
                    item
                )

                continue

            request = item._request

            # -------------------------------------------------
            # Sync file progress
            # -------------------------------------------------

            self._sync_file_progress(
                item
            )

            # -------------------------------------------------
            # Pause live request
            # -------------------------------------------------

            if request is not None:

                request_id = id(
                    request
                )

                self._pausing_requests.add(
                    request_id
                )

                try:

                    request.pause()

                except Exception as exc:

                    print(
                        "⚠️ DOWNLOAD PAUSE FAILED:",
                        exc,
                    )

                    self._pausing_requests.discard(
                        request_id
                    )

            # -------------------------------------------------
            # Model
            # -------------------------------------------------

            item.pause()

            item.speed = 0.0

            item.remaining_seconds = -1

            # -------------------------------------------------
            # Persist
            # -------------------------------------------------

            self._persist_item(
                item
            )

            self.download_updated.emit(
                item
            )

    # =========================================================
    # Resume After Restart
    # =========================================================

    def resume_download(
        self,
        item_id: int,
    ) -> bool:
        """
        Resume a persisted download using HTTP Range.
        """

        item = self._find_download(
            item_id
        )

        if item is None:

            print(
                "❌ RESUME FAILED: DOWNLOAD NOT FOUND"
            )

            return False

        # -----------------------------------------------------
        # Valid states
        # -----------------------------------------------------

        if item.state not in (
            "paused",
            "interrupted",
        ):

            print(
                "⚠️ RESUME IGNORED:"
                f" state={item.state}"
            )

            return False

        # -----------------------------------------------------
        # Already running
        # -----------------------------------------------------

        if self._resume_replies.get(
            item.id
        ) is not None:

            print(
                f"⚠️ DOWNLOAD ALREADY RESUMED: "
                f"{item.filename}"
            )

            return False

        # -----------------------------------------------------
        # Clear stale pause marker
        # -----------------------------------------------------

        self._pausing_resume_ids.discard(
            item.id
        )

        # -----------------------------------------------------
        # Determine actual local size
        # -----------------------------------------------------

        path = Path(
            item.full_path
        )

        if path.exists():

            try:

                item.received_bytes = (
                    path.stat().st_size
                )

            except OSError as exc:

                print(
                    "❌ FAILED TO READ DOWNLOAD SIZE:",
                    exc,
                )

                return False

        else:

            item.received_bytes = 0

            try:

                path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

            except OSError as exc:

                print(
                    "❌ FAILED TO CREATE DOWNLOAD DIRECTORY:",
                    exc,
                )

                return False

        # -----------------------------------------------------
        # Already complete
        # -----------------------------------------------------

        if (
            item.total_bytes > 0
            and item.received_bytes >= item.total_bytes
        ):

            item.received_bytes = (
                item.total_bytes
            )

            item.progress = 100.0

            item.finish()

            item.remaining_seconds = 0

            self._persist_item(
                item
            )

            self.download_updated.emit(
                item
            )

            self.download_finished.emit(
                item
            )

            return True

        # -----------------------------------------------------
        # Build Range request
        # -----------------------------------------------------

        start_byte = max(
            0,
            item.received_bytes,
        )

        request = QNetworkRequest(
            QUrl(
                item.url
            )
        )

        request.setRawHeader(
            QByteArray(
                b"Range"
            ),
            QByteArray(
                f"bytes={start_byte}-".encode()
            ),
        )

        # -----------------------------------------------------
        # Diagnostics
        # -----------------------------------------------------

        print(
            "▶️ RESUME DOWNLOAD:"
        )

        print(
            "FILE:",
            item.filename,
        )

        print(
            "LOCAL SIZE:",
            start_byte,
        )

        print(
            "RANGE:",
            f"bytes={start_byte}-",
        )

        # -----------------------------------------------------
        # Start network request
        # -----------------------------------------------------

        reply = self._network_manager.get(
            request
        )

        self._resume_replies[
            item.id
        ] = reply

        # -----------------------------------------------------
        # Model state
        # -----------------------------------------------------

        item.paused = False

        item.canceled = False

        item.interrupted = False

        item.finished = False

        item.successful = False

        item.state = "downloading"

        item.speed = 0.0

        item.remaining_seconds = -1

        item.touch()

        # -----------------------------------------------------
        # Progress timing
        # -----------------------------------------------------

        self._last_progress[
            item.id
        ] = (
            item.received_bytes,
            monotonic(),
        )

        # -----------------------------------------------------
        # Persist
        # -----------------------------------------------------

        self._persist_item(
            item
        )

        # -----------------------------------------------------
        # Signals
        # -----------------------------------------------------

        reply.readyRead.connect(
            lambda: self._resume_ready_read(
                item,
                reply,
            )
        )

        reply.finished.connect(
            lambda: self._resume_finished(
                item,
                reply,
            )
        )

        reply.errorOccurred.connect(
            lambda error: self._resume_error(
                item,
                reply,
                error,
            )
        )

        # -----------------------------------------------------
        # UI
        # -----------------------------------------------------

        self.download_updated.emit(
            item
        )

        return True

    # =========================================================
    # Resume Data
    # =========================================================

    def _resume_ready_read(
        self,
        item: DownloadItem,
        reply: QNetworkReply,
    ) -> None:
        """
        Read and append resumed network data.
        """

        # -----------------------------------------------------
        # Intentional pause / shutdown
        # -----------------------------------------------------

        if item.id in self._pausing_resume_ids:

            try:

                reply.readAll()

            except Exception:

                pass

            return

        # -----------------------------------------------------
        # HTTP status
        # -----------------------------------------------------

        status = reply.attribute(
            QNetworkRequest.HttpStatusCodeAttribute
        )

        if status not in (
            206,
            None,
        ):

            return

        # -----------------------------------------------------
        # Read data
        # -----------------------------------------------------

        data = reply.readAll()

        if not data:

            return

        # -----------------------------------------------------
        # File
        # -----------------------------------------------------

        path = Path(
            item.full_path
        )

        try:

            path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with path.open(
                "ab"
            ) as file:

                file.write(
                    bytes(data)
                )

        except OSError as exc:

            print(
                "❌ FAILED TO WRITE RESUME DATA:",
                exc,
            )

            return

        # -----------------------------------------------------
        # Actual file size
        # -----------------------------------------------------

        try:

            item.received_bytes = (
                path.stat().st_size
            )

        except OSError as exc:

            print(
                "⚠️ FAILED TO READ RESUME FILE SIZE:",
                exc,
            )

            return

        # -----------------------------------------------------
        # Progress
        # -----------------------------------------------------

        if item.total_bytes > 0:

            item.progress = min(
                100.0,
                (
                    item.received_bytes
                    / item.total_bytes
                )
                * 100.0,
            )

        # -----------------------------------------------------
        # Speed
        # -----------------------------------------------------

        now = monotonic()

        previous = self._last_progress.get(
            item.id
        )

        if previous is not None:

            previous_bytes, previous_time = previous

            elapsed = (
                now
                - previous_time
            )

            delta = (
                item.received_bytes
                - previous_bytes
            )

            if (
                elapsed > 0
                and delta >= 0
            ):

                item.speed = (
                    delta
                    / elapsed
                )

        self._last_progress[
            item.id
        ] = (
            item.received_bytes,
            now,
        )

        # -----------------------------------------------------
        # ETA
        # -----------------------------------------------------

        if (
            item.speed > 0
            and item.total_bytes > item.received_bytes
        ):

            item.remaining_seconds = int(
                (
                    item.total_bytes
                    - item.received_bytes
                )
                / item.speed
            )

        else:

            item.remaining_seconds = -1

        item.touch()

        # -----------------------------------------------------
        # Persistence
        # -----------------------------------------------------

        self._persist_progress(
            item
        )

        # -----------------------------------------------------
        # UI
        # -----------------------------------------------------

        self.download_updated.emit(
            item
        )

    # =========================================================
    # Resume Finished
    # =========================================================

    def _resume_finished(
        self,
        item: DownloadItem,
        reply: QNetworkReply,
    ) -> None:
        """
        Handle completion of a resumed download.
        """

        # =====================================================
        # Intentional Pause
        # =====================================================

        if item.id in self._pausing_resume_ids:

            print(
                f"⏸️ RESUME REPLY PAUSED: "
                f"{item.filename}"
            )

            self._pausing_resume_ids.discard(
                item.id
            )

            self._sync_file_progress(
                item
            )

            item.state = "paused"

            item.paused = True

            item.canceled = False

            item.interrupted = False

            item.finished = False

            item.successful = False

            item.speed = 0.0

            item.remaining_seconds = -1

            item.touch()

            self._persist_item(
                item
            )

            self._cleanup_resume_reply(
                item.id,
                reply,
            )

            self.download_updated.emit(
                item
            )

            return

        # =====================================================
        # Network error
        # =====================================================

        if reply.error():

            print(
                f"❌ RESUME DOWNLOAD ERROR: "
                f"{item.filename}"
            )

            print(
                "ERROR:",
                reply.errorString(),
            )

            self._sync_file_progress(
                item
            )

            item.state = "paused"

            item.paused = True

            item.canceled = False

            item.interrupted = False

            item.speed = 0.0

            item.remaining_seconds = -1

            item.touch()

            self._persist_item(
                item
            )

            self._cleanup_resume_reply(
                item.id,
                reply,
            )

            self.download_updated.emit(
                item
            )

            self.download_failed.emit(
                item
            )

            return

        # =====================================================
        # HTTP status
        # =====================================================

        status = reply.attribute(
            QNetworkRequest.HttpStatusCodeAttribute
        )

        # =====================================================
        # HTTP 206
        # =====================================================

        if status == 206:

            self._sync_file_progress(
                item
            )

            if (
                item.total_bytes > 0
                and item.received_bytes >= item.total_bytes
            ):

                item.received_bytes = (
                    item.total_bytes
                )

                item.finish()

                item.remaining_seconds = 0

                self._persist_item(
                    item
                )

                self.download_updated.emit(
                    item
                )

                self.download_finished.emit(
                    item
                )

            else:

                print(
                    f"⏸️ RESUME RESPONSE FINISHED "
                    f"BEFORE COMPLETION: "
                    f"{item.filename}"
                )

                item.state = "paused"

                item.paused = True

                item.canceled = False

                item.interrupted = False

                item.speed = 0.0

                item.remaining_seconds = -1

                item.touch()

                self._persist_item(
                    item
                )

                self.download_updated.emit(
                    item
                )

        # =====================================================
        # HTTP 200
        #
        # Server ignored Range.
        #
        # IMPORTANT:
        # We do not append this response to the partial file.
        # =====================================================

        elif status == 200:

            print(
                f"⚠️ SERVER IGNORED RANGE: "
                f"{item.filename}"
            )

            item.state = "paused"

            item.paused = True

            item.canceled = False

            item.interrupted = False

            item.speed = 0.0

            item.remaining_seconds = -1

            item.touch()

            self._persist_item(
                item
            )

            self.download_updated.emit(
                item
            )

        # =====================================================
        # Other status
        # =====================================================

        else:

            print(
                f"⚠️ RESUME HTTP STATUS {status}: "
                f"{item.filename}"
            )

            item.state = "paused"

            item.paused = True

            item.canceled = False

            item.interrupted = False

            item.speed = 0.0

            item.remaining_seconds = -1

            item.touch()

            self._persist_item(
                item
            )

            self.download_updated.emit(
                item
            )

        # =====================================================
        # Cleanup
        # =====================================================

        self._cleanup_resume_reply(
            item.id,
            reply,
        )

    # =========================================================
    # Resume Error
    # =========================================================

    def _resume_error(
        self,
        item: DownloadItem,
        reply: QNetworkReply,
        error,
    ) -> None:
        """
        Handle QNetworkReply errors.

        The actual state transition is handled in
        _resume_finished().
        """

        if item.id in self._pausing_resume_ids:

            return

        print(
            "⚠️ RESUME NETWORK ERROR:",
            error,
        )

    # =========================================================
    # Persistence
    # =========================================================

    def _persist_add(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Persist a newly created download.
        """

        try:

            self.repository.add(
                item
            )

        except Exception as exc:

            print(
                "❌ FAILED TO ADD DOWNLOAD:",
                exc,
            )

    # ---------------------------------------------------------

    def _persist_item(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Persist complete DownloadItem state.
        """

        try:

            self.repository.update(
                item
            )

        except Exception as exc:

            print(
                "❌ FAILED TO UPDATE DOWNLOAD:",
                exc,
            )

    # ---------------------------------------------------------

    def _persist_progress(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Persist download progress.
        """

        try:

            self.repository.update_progress(
                item
            )

        except Exception as exc:

            print(
                "❌ FAILED TO SAVE DOWNLOAD PROGRESS:",
                exc,
            )

    # =========================================================
    # File Synchronization
    # =========================================================

    def _sync_file_progress(
        self,
        item: DownloadItem,
    ) -> None:
        """
        Synchronize received_bytes with the actual file size.
        """

        path = Path(
            item.full_path
        )

        if not path.exists():

            return

        try:

            actual_size = (
                path.stat().st_size
            )

        except OSError as exc:

            print(
                "⚠️ FAILED TO READ DOWNLOAD FILE SIZE:",
                exc,
            )

            return

        item.received_bytes = (
            actual_size
        )

        if item.total_bytes > 0:

            item.progress = min(
                100.0,
                (
                    actual_size
                    / item.total_bytes
                )
                * 100.0,
            )

    # =========================================================
    # Lookup
    # =========================================================

    def _find_download(
        self,
        item_id: int,
    ) -> DownloadItem | None:
        """
        Find a DownloadItem by database ID.
        """

        for item in self._downloads:

            if item.id == item_id:

                return item

        return None

    # =========================================================
    # Resume Cleanup
    # =========================================================

    def _cleanup_resume_reply(
        self,
        item_id: int,
        reply: QNetworkReply,
    ) -> None:
        """
        Remove and safely dispose of a resume reply.
        """

        self._resume_replies.pop(
            item_id,
            None,
        )

        self._pausing_resume_ids.discard(
            item_id
        )

        if reply is not None:

            reply.deleteLater()

    # =========================================================
    # History
    # =========================================================

    def _load_downloads(
        self,
    ) -> None:
        """
        Restore persisted download history.
        """

        try:

            downloads = (
                self.repository.all_downloads()
            )

            self._downloads.extend(
                downloads
            )

            print(
                "📥 DOWNLOAD HISTORY LOADED:",
                len(downloads),
            )

        except Exception as exc:

            print(
                "❌ DOWNLOAD HISTORY LOAD FAILED:",
                exc,
            )

    # =========================================================
    # Shutdown
    # =========================================================

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown the DownloadManager.

        pause_all_active() should be called before shutdown().
        """

        print(
            "🧹 DOWNLOAD MANAGER SHUTDOWN"
        )

        # -----------------------------------------------------
        # Abort active resume replies
        # -----------------------------------------------------

        for item_id, reply in list(
            self._resume_replies.items()
        ):

            if reply is None:

                continue

            self._pausing_resume_ids.add(
                item_id
            )

            try:

                reply.abort()

            except Exception as exc:

                print(
                    "⚠️ FAILED TO ABORT RESUME REPLY:",
                    exc,
                )

        # -----------------------------------------------------
        # Clear runtime collections
        # -----------------------------------------------------

        self._resume_replies.clear()

        self._pausing_resume_ids.clear()

        self._accepted_requests.clear()

        self._pausing_requests.clear()

        self._last_progress.clear()

        print(
            "✅ DOWNLOAD MANAGER SHUTDOWN COMPLETED"
        )

    # =========================================================
    # Formatting Helpers
    # =========================================================

    @staticmethod
    def format_size(
        value: float | int,
    ) -> str:
        """
        Format byte size for UI.
        """

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

        if value < 1024 ** 4:

            return (
                f"{value / (1024 ** 3):.2f} GB"
            )

        return (
            f"{value / (1024 ** 4):.2f} TB"
        )

    # ---------------------------------------------------------

    @staticmethod
    def format_speed(
        value: float | int,
    ) -> str:
        """
        Format download speed.
        """

        value = max(
            0,
            float(value),
        )

        return (
            DownloadManager.format_size(
                value
            )
            + "/s"
        )

    # ---------------------------------------------------------

    @staticmethod
    def format_eta(
        seconds: int | float,
    ) -> str:
        """
        Format remaining download time.
        """

        if (
            seconds is None
            or seconds < 0
        ):

            return "--"

        seconds = int(
            seconds
        )

        if seconds < 60:

            return f"{seconds}s"

        minutes, seconds = divmod(
            seconds,
            60,
        )

        if minutes < 60:

            return (
                f"{minutes}m {seconds}s"
            )

        hours, minutes = divmod(
            minutes,
            60,
        )

        return (
            f"{hours}h {minutes}m"
        )
