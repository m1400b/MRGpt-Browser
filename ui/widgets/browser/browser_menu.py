"""
MRGpt Browser

Browser Menu
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QMenu,
    QWidget,
)


class BrowserMenu(QMenu):
    """
    Main browser menu.

    مسئول ساختار منوی مرورگر است و مستقیماً
    به Browser یا Serviceها وابستگی ندارد.
    """

    # -------------------------------------------------
    # Signals
    # -------------------------------------------------

    downloads_requested = Signal()

    settings_requested = Signal()

    exit_requested = Signal()

    # =================================================
    # Constructor
    # =================================================

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(
            parent
        )

        self.setTitle(
            "Menu"
        )

        self._create_actions()

        self._build_menu()

        self._connect_signals()

    # =================================================
    # Actions
    # =================================================

    def _create_actions(self) -> None:

        self.downloads_action = self.addAction(
            "Downloads"
        )

        self.addSeparator()

        self.settings_action = self.addAction(
            "Settings"
        )

        self.addSeparator()

        self.exit_action = self.addAction(
            "Exit"
        )

    # =================================================
    # Menu
    # =================================================

    def _build_menu(self) -> None:
        """
        Menu structure is currently created
        through actions in _create_actions().
        """

        pass

    # =================================================
    # Signals
    # =================================================

    def _connect_signals(self) -> None:

        self.downloads_action.triggered.connect(
            self.downloads_requested.emit
        )

        self.settings_action.triggered.connect(
            self.settings_requested.emit
        )

        self.exit_action.triggered.connect(
            self.exit_requested.emit
        )