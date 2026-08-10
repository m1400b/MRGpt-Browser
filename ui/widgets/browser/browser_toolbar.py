
"""
MRGpt Browser

Browser Toolbar
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal, QUrl
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
)

from ui.widgets.browser.address_bar import AddressBar


class BrowserToolbar(QWidget):
    """
    Browser Toolbar

    فقط مسئول رابط کاربری است و هیچ وابستگی مستقیمی
    به Browser، Controller یا MainWindow ندارد.
    """

    # -------------------------------------------------
    # Signals
    # -------------------------------------------------

    new_tab_requested = Signal()

    back_requested = Signal()

    forward_requested = Signal()

    reload_requested = Signal()

    home_requested = Signal()

    ai_requested = Signal()

    menu_requested = Signal()

    settings_requested = Signal()

    navigate_requested = Signal(str)

    # -------------------------------------------------

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self._create_widgets()

        self._build_ui()

        self._connect_signals()

    # =================================================
    # Button Factory
    # =================================================

    def _create_button(
        self,
        text: str,
        tooltip: str,
    ) -> QPushButton:

        button = QPushButton(text)

        button.setToolTip(tooltip)

        button.setFixedSize(
            34,
            34,
        )

        button.setFocusPolicy(
            Qt.NoFocus
        )

        button.setCursor(
            Qt.PointingHandCursor
        )

        return button

    # =================================================
    # Widgets
    # =================================================

    def _create_widgets(self) -> None:

        self.back_button = self._create_button(
            "◀",
            "Back",
        )

        self.forward_button = self._create_button(
            "▶",
            "Forward",
        )

        self.reload_button = self._create_button(
            "⟳",
            "Reload",
        )

        self.home_button = self._create_button(
            "⌂",
            "Home",
        )

        self.new_tab_button = self._create_button(
            "🗋",
            "New Tab",
        )

        self.address_bar = AddressBar()

        self.ai_button = self._create_button(
            "🤖",
            "AI Assistant",
        )

        self.settings_button = self._create_button(
            "⚙",
            "Settings",
        )

        self.menu_button = self._create_button(
            "☰",
            "Menu",
        )

    # =================================================
    # UI
    # =================================================

    def _build_ui(self) -> None:

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            6,
            6,
            6,
            6,
        )

        layout.setSpacing(6)

        layout.addWidget(
            self.back_button
        )

        layout.addWidget(
            self.forward_button
        )

        layout.addWidget(
            self.reload_button
        )

        layout.addWidget(
            self.home_button
        )

        layout.addWidget(
            self.address_bar,
            1,
        )

        layout.addWidget(
            self.new_tab_button
        )

        layout.addWidget(
            self.ai_button
        )

        layout.addWidget(
            self.settings_button
        )

        layout.addWidget(
            self.menu_button
        )

    # =================================================
    # Signals
    # =================================================

    def _connect_signals(self) -> None:

        self.new_tab_button.clicked.connect(
            self.new_tab_requested.emit
        )

        self.back_button.clicked.connect(
            self.back_requested.emit
        )

        self.forward_button.clicked.connect(
            self.forward_requested.emit
        )

        self.reload_button.clicked.connect(
            self.reload_requested.emit
        )

        self.home_button.clicked.connect(
            self.home_requested.emit
        )

        self.ai_button.clicked.connect(
            self.ai_requested.emit
        )

        self.settings_button.clicked.connect(
            self.settings_requested.emit
        )

        self.menu_button.clicked.connect(
            self.menu_requested.emit
        )

        self.address_bar.navigate_requested.connect(
            self.navigate_requested.emit
        )

    # =================================================
    # Address Bar
    # =================================================

    def set_url(
        self,
        url: str | QUrl,
    ) -> None:

        self.address_bar.set_url(
            url
        )

    # -------------------------------------------------

    def url(self) -> str:

        return self.address_bar.url()

    # -------------------------------------------------

    def clear_url(self) -> None:

        self.address_bar.clear_url()

    # -------------------------------------------------

    def focus_address_bar(self) -> None:

        self.address_bar.setFocus()

    # -------------------------------------------------

    def select_address(self) -> None:

        self.address_bar.select_all()

    # =================================================
    # Loading
    # =================================================

    def set_loading(
        self,
        loading: bool,
    ) -> None:

        self.reload_button.setText(
            "✕" if loading else "⟳"
        )

    # =================================================
    # Navigation
    # =================================================

    def set_navigation_state(
        self,
        can_go_back: bool,
        can_go_forward: bool,
    ) -> None:

        self.back_button.setEnabled(
            can_go_back
        )

        self.forward_button.setEnabled(
            can_go_forward
        )

