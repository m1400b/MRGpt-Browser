"""
MRGpt Browser

Global Event Bus
"""

from __future__ import annotations

from collections import defaultdict

from threading import RLock

from typing import Callable

from core.events.event import Event


class EventBus:
    """
    Global Event Dispatcher
    """

    # -------------------------------------------------

    _instance = None

    # -------------------------------------------------

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance

    # -------------------------------------------------

    def __init__(self):

        if hasattr(self, "_initialized"):

            return

        self._initialized = True

        self._listeners = defaultdict(list)

        self._lock = RLock()

    # =================================================
    # Subscribe
    # =================================================

    def subscribe(

        self,

        event_name: str,

        callback: Callable,

        priority: int = 100,

    ):

        with self._lock:

            self._listeners[event_name].append(

                (

                    priority,

                    callback,

                )

            )

            self._listeners[event_name].sort(

                key=lambda item: item[0]

            )

    # =================================================
    # Unsubscribe
    # =================================================

    def unsubscribe(

        self,

        event_name: str,

        callback: Callable,

    ):

        with self._lock:

            listeners = self._listeners.get(

                event_name,

                [],

            )

            self._listeners[event_name] = [

                item

                for item in listeners

                if item[1] != callback

            ]

    # =================================================
    # Publish
    # =================================================

    def publish(

        self,

        event: Event,

    ):

        with self._lock:

            listeners = list(

                self._listeners.get(

                    event.name,

                    []

                )

            )

        for _, callback in listeners:

            if event.is_cancelled:

                break

            try:

                callback(event)

            except Exception as ex:

                print(

                    f"[EventBus] {event.name}:",

                    ex

                )

    # =================================================
    # Clear
    # =================================================

    def clear(self):

        with self._lock:

            self._listeners.clear()

    # =================================================
    # Count
    # =================================================

    def listener_count(

        self,

        event_name: str,

    ) -> int:

        return len(

            self._listeners.get(

                event_name,

                []

            )

        )

    # =================================================
    # Registered
    # =================================================

    def has_listener(

        self,

        event_name: str,

    ) -> bool:

        return (

            self.listener_count(

                event_name

            )

            > 0

        )

    # =================================================
    # Events
    # =================================================

    @property
    def events(self):

        return tuple(

            self._listeners.keys()

        )


# ---------------------------------------------------------
# Global Singleton
# ---------------------------------------------------------

event_bus = EventBus()