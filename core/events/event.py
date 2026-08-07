"""
MRGpt Browser

Base Event
"""

from __future__ import annotations

from dataclasses import dataclass, field

from datetime import datetime
from uuid import uuid4

from typing import Any


@dataclass(slots=True)
class Event:
    """
    Base Event
    """

    # -----------------------------------------

    name: str

    # -----------------------------------------

    source: str = ""

    # -----------------------------------------

    payload: dict[str, Any] = field(
        default_factory=dict
    )

    # -----------------------------------------

    event_id: str = field(
        default_factory=lambda: str(
            uuid4()
        )
    )

    # -----------------------------------------

    timestamp: datetime = field(
        default_factory=datetime.now
    )

    # -----------------------------------------

    handled: bool = False

    # -----------------------------------------

    cancelled: bool = False

    # -------------------------------------------------

    def get(

        self,

        key: str,

        default=None,

    ):

        return self.payload.get(

            key,

            default

        )

    # -------------------------------------------------

    def set(

        self,

        key: str,

        value,

    ):

        self.payload[key] = value

    # -------------------------------------------------

    def cancel(self):

        self.cancelled = True

    # -------------------------------------------------

    def mark_handled(self):

        self.handled = True

    # -------------------------------------------------

    @property
    def is_cancelled(self):

        return self.cancelled

    # -------------------------------------------------

    @property
    def is_handled(self):

        return self.handled

    # -------------------------------------------------

    def __getitem__(

        self,

        key,

    ):

        return self.payload[key]

    # -------------------------------------------------

    def __setitem__(

        self,

        key,

        value,

    ):

        self.payload[key] = value

    # -------------------------------------------------

    def __contains__(

        self,

        key,

    ):

        return key in self.payload

    # -------------------------------------------------

    def __repr__(self):

        return (

            f"<Event "

            f"name={self.name!r} "

            f"source={self.source!r} "

            f"handled={self.handled} "

            f"cancelled={self.cancelled}>"

        )