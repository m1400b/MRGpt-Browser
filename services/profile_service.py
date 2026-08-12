"""
MRGpt Browser

Profile Service
"""

from __future__ import annotations

from typing import Dict, Optional

from PySide6.QtCore import QObject, Signal

from core.profile.browser_profile import BrowserProfile


class ProfileService(QObject):
    """
    مدیریت تمامی Browser Profile ها
    """

    profile_created = Signal(str)

    profile_removed = Signal(str)

    current_profile_changed = Signal(str)

    # ---------------------------------------------------------

    def __init__(self, parent=None):

        super().__init__(parent)

        self._profiles: Dict[str, BrowserProfile] = {}

        self._current_name: Optional[str] = None

    # ---------------------------------------------------------

    def register(
        self,
        name: str,
        profile: BrowserProfile
    ) -> None:

        if name in self._profiles:

            raise ValueError(
                f'Profile "{name}" already exists.'
            )

        self._profiles[name] = profile

        if self._current_name is None:

            self._current_name = name

        self.profile_created.emit(name)

    # ---------------------------------------------------------

    def unregister(
        self,
        name: str
    ) -> None:

        if name not in self._profiles:
            return

        del self._profiles[name]

        self.profile_removed.emit(name)

        if self._current_name == name:

            self._current_name = None

            if self._profiles:

                self._current_name = next(
                    iter(self._profiles)
                )

                self.current_profile_changed.emit(
                    self._current_name
                )

    # ---------------------------------------------------------

    def set_current(
        self,
        name: str
    ) -> None:

        if name not in self._profiles:

            raise KeyError(
                f'Profile "{name}" not found.'
            )

        self._current_name = name

        self.current_profile_changed.emit(name)

    # ---------------------------------------------------------

    def current(self) -> BrowserProfile:

        if self._current_name is None:

            raise RuntimeError(
                "No active profile."
            )

        return self._profiles[self._current_name]

    # ---------------------------------------------------------

    def get(
        self,
        name: str
    ) -> Optional[BrowserProfile]:

        return self._profiles.get(name)

    # ---------------------------------------------------------

    def exists(
        self,
        name: str
    ) -> bool:

        return name in self._profiles

    # ---------------------------------------------------------

    def names(self) -> list[str]:

        return sorted(self._profiles.keys())

    # ---------------------------------------------------------

    def profiles(self) -> Dict[str, BrowserProfile]:

        return self._profiles.copy()

    # ---------------------------------------------------------

    def count(self) -> int:

        return len(self._profiles)

    # ---------------------------------------------------------

    def clear(self) -> None:

        self._profiles.clear()

        self._current_name = None

    # ---------------------------------------------------------

    @property
    def current_name(self) -> Optional[str]:

        return self._current_name
    
    # =================================================
    # Shutdown
    # =================================================
    
    def shutdown(self) -> None:
        """
        Shutdown all registered browser profiles.
    
        Profiles are released only after browser tabs/pages
        have already been closed by the Browser facade.
        """
    
        self._profiles.clear()
    
        self._current_name = None