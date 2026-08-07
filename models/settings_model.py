"""
MRGpt Browser

Settings Model
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from models.base_model import BaseModel


@dataclass(slots=True)
class SettingsModel(BaseModel):
    """
    Base class for all application settings.
    """

    version: str = "1.0"

    schema: int = 1

    last_modified: datetime = field(
        default_factory=datetime.now
    )

    # -------------------------------------------------

    def touch(self):
        """
        Update modification time.
        """

        self.last_modified = datetime.now()

    # -------------------------------------------------

    def reset(self):
        """
        Reset settings.

        Child classes should override this method.
        """

        self.touch()