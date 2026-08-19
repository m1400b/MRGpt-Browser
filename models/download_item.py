"""
MRGpt Browser

Download Item Model
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from models.entity_model import EntityModel


@dataclass(slots=True)
class DownloadItem(EntityModel):
    """
    Browser Download Item.

    Represents a browser download both during runtime
    and when persisted in the application database.
    """

    # =================================================
    # File Information
    # =================================================

    filename: str = ""

    url: str = ""

    directory: str = ""

    mime_type: str = ""

    # =================================================
    # Download Information
    # =================================================

    total_bytes: int = 0

    received_bytes: int = 0

    progress: float = 0.0

    speed: float = 0.0

    remaining_seconds: int = -1

    # =================================================
    # State
    # =================================================

    state: str = "waiting"

    paused: bool = False

    finished: bool = False

    successful: bool = False

    canceled: bool = False

    interrupted: bool = False

    # =================================================
    # Time
    # =================================================

    started_at: datetime = field(
        default_factory=datetime.now
    )

    finished_at: datetime | None = None

    # =================================================
    # Runtime
    # =================================================

    _request: object | None = field(
        default=None,
        repr=False,
        compare=False,
    )

    # =================================================
    # File Path
    # =================================================

    @property
    def full_path(self) -> str:
        """
        Return the complete download file path.
        """

        if not self.directory:

            return self.filename

        return str(
            Path(self.directory) / self.filename
        )

    # =================================================
    # Status
    # =================================================

    @property
    def is_active(self) -> bool:
        """
        Return True when the download is currently
        active or paused.

        A paused download is still considered active
        because it can be resumed.
        """

        return self.state in (
            "waiting",
            "downloading",
            "paused",
        )

    # -------------------------------------------------

    @property
    def is_completed(self) -> bool:
        """
        Return True when the download completed
        successfully.
        """

        return self.state == "completed"

    # -------------------------------------------------

    @property
    def is_failed(self) -> bool:
        """
        Return True when the download was interrupted
        or failed.
        """

        return self.state in (
            "interrupted",
            "failed",
        )

    # -------------------------------------------------

    @property
    def is_canceled(self) -> bool:
        """
        Return True when the download was canceled.
        """

        return self.state == "canceled"

    # =================================================
    # Progress
    # =================================================

    def update_progress(
        self,
        received: int,
        total: int,
    ) -> None:
        """
        Update download progress.
        """

        self.received_bytes = max(
            0,
            received,
        )

        self.total_bytes = max(
            0,
            total,
        )

        if self.total_bytes > 0:

            self.progress = (
                self.received_bytes
                / self.total_bytes
            ) * 100.0

            self.progress = min(
                100.0,
                self.progress,
            )

        else:

            self.progress = 0.0

        self.touch()

    # =================================================
    # State Transitions
    # =================================================

    def start(self) -> None:
        """
        Mark the download as started.
        """

        self.state = "downloading"

        self.paused = False

        self.finished = False

        self.successful = False

        self.canceled = False

        self.interrupted = False

        if self.started_at is None:

            self.started_at = datetime.now()

        self.touch()

    # -------------------------------------------------

    def finish(self) -> None:
        """
        Mark the download as successfully completed.
        """

        self.state = "completed"

        self.paused = False

        self.finished = True

        self.successful = True

        self.canceled = False

        self.interrupted = False

        self.progress = 100.0

        self.finished_at = datetime.now()

        self.touch()

    # -------------------------------------------------

    def cancel(self) -> None:
        """
        Mark the download as canceled.
        """

        self.state = "canceled"

        self.paused = False

        self.finished = False

        self.successful = False

        self.canceled = True

        self.interrupted = False

        self.finished_at = datetime.now()

        self.touch()

    # -------------------------------------------------

    def interrupt(self) -> None:
        """
        Mark the download as interrupted.
        """

        self.state = "interrupted"

        self.paused = False

        self.finished = False

        self.successful = False

        self.canceled = False

        self.interrupted = True

        self.finished_at = datetime.now()

        self.touch()

    # -------------------------------------------------

    def fail(self) -> None:
        """
        Mark the download as failed.
        """

        self.state = "failed"

        self.paused = False

        self.finished = False

        self.successful = False

        self.canceled = False

        self.interrupted = True

        self.finished_at = datetime.now()

        self.touch()

    # -------------------------------------------------

    def pause(self) -> None:
        """
        Pause the download.
        """

        if not self.is_active:

            return

        self.paused = True

        self.state = "paused"

        self.touch()

    # -------------------------------------------------

    def resume(self) -> None:
        """
        Resume a paused download.
        """

        if self.state != "paused":

            return

        self.paused = False

        self.state = "downloading"

        self.touch()

    # =================================================
    # Persistence Helpers
    # =================================================

    @property
    def save_path(self) -> str:
        """
        Return the complete path used for persistence.
        """

        return self.full_path

    # -------------------------------------------------

    @property
    def file_name(self) -> str:
        """
        Compatibility alias for repository/database
        naming.
        """

        return self.filename

    # -------------------------------------------------

    @property
    def created_at(self) -> datetime:
        """
        Persistence-compatible creation timestamp.
        """

        return self.started_at

    # -------------------------------------------------

    @property
    def updated_at(self) -> datetime:
        """
        Persistence-compatible update timestamp.

        EntityModel.touch() updates the model timestamp.
        """

        return getattr(
            self,
            "_updated_at",
            self.started_at,
        )

    # =================================================
    # String Representation
    # =================================================

    def __str__(self) -> str:
        return (
            f"{self.filename} "
            f"({self.progress:.1f}%)"
        )

