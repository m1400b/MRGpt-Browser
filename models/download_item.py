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
    Browser Download Item
    """

    # -------------------------------------------------
    # File Information
    # -------------------------------------------------

    filename: str = ""

    url: str = ""

    directory: str = ""

    mime_type: str = ""

    # -------------------------------------------------
    # Download Information
    # -------------------------------------------------

    total_bytes: int = 0

    received_bytes: int = 0

    progress: float = 0.0

    speed: float = 0.0

    remaining_seconds: int = -1

    # -------------------------------------------------
    # State
    # -------------------------------------------------

    state: str = "waiting"

    paused: bool = False

    finished: bool = False

    successful: bool = False

    canceled: bool = False

    interrupted: bool = False

    # -------------------------------------------------
    # Time
    # -------------------------------------------------

    started_at: datetime = field(
        default_factory=datetime.now
    )

    finished_at: datetime | None = None

    # -------------------------------------------------
    # Internal
    # -------------------------------------------------

    _request: object | None = field(
        default=None,
        repr=False
    )

    # -------------------------------------------------

    @property
    def full_path(self) -> str:
        """
        Complete file path.
        """

        if not self.directory:

            return self.filename

        return str(

            Path(self.directory) / self.filename

        )

    # -------------------------------------------------

    @property
    def is_active(self) -> bool:

        return not (

            self.finished
            or self.canceled
            or self.interrupted

        )

    # -------------------------------------------------

    def update_progress(
        self,
        received: int,
        total: int
    ):

        self.received_bytes = received

        self.total_bytes = total

        if total > 0:

            self.progress = (

                received / total

            ) * 100

        self.touch()

    # -------------------------------------------------

    def finish(self):

        self.finished = True

        self.successful = True

        self.state = "finished"

        self.finished_at = datetime.now()

        self.touch()

    # -------------------------------------------------

    def cancel(self):

        self.canceled = True

        self.state = "canceled"

        self.finished_at = datetime.now()

        self.touch()

    # -------------------------------------------------

    def interrupt(self):

        self.interrupted = True

        self.state = "interrupted"

        self.finished_at = datetime.now()

        self.touch()

    # -------------------------------------------------

    def pause(self):

        self.paused = True

        self.state = "paused"

        self.touch()

    # -------------------------------------------------

    def resume(self):

        self.paused = False

        self.state = "downloading"

        self.touch()

    # -------------------------------------------------

    def __str__(self):

        return f"{self.filename} ({self.progress:.1f}%)"