"""
MRGpt Browser

History Item Model
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from models.base_model import BaseModel


@dataclass(slots=True)
class HistoryItem(BaseModel):
    """
    Browser History Record
    """

    id: int = 0

    url: str = ""

    title: str = ""

    visit_time: datetime = field(
        default_factory=datetime.now
    )

    favicon: str = ""

    visit_count: int = 1

    # -------------------------------------------------

    @property
    def domain(self) -> str:
        """
        Website domain.
        """

        if "://" not in self.url:
            return self.url

        return self.url.split("/")[2]

    # -------------------------------------------------

    def increase_visit(self):

        self.visit_count += 1

    # -------------------------------------------------

    @property
    def is_empty(self) -> bool:

        return self.url == ""

    # -------------------------------------------------

    def __str__(self):

        return f"{self.title} ({self.url})"