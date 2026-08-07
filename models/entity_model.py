"""
MRGpt Browser

Entity Model
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from models.base_model import BaseModel


@dataclass(slots=True)
class EntityModel(BaseModel):
    """
    Base class for all database entities.
    """

    id: int = 0

    uuid: str = field(
        default_factory=lambda: str(uuid4())
    )

    created_at: datetime = field(
        default_factory=datetime.now
    )

    updated_at: datetime = field(
        default_factory=datetime.now
    )

    is_deleted: bool = False

    # -------------------------------------------------

    def touch(self):
        """
        Update modification time.
        """

        self.updated_at = datetime.now()

    # -------------------------------------------------

    def delete(self):
        """
        Soft Delete
        """

        self.is_deleted = True

        self.touch()

    # -------------------------------------------------

    def restore(self):
        """
        Restore entity.
        """

        self.is_deleted = False

        self.touch()

    # -------------------------------------------------

    @property
    def is_new(self) -> bool:

        return self.id == 0