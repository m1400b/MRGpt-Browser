"""
MRGpt Browser

Settings Dialog
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QTabWidget,
    QVBoxLayout,
)

from services.settings_service import SettingsService
from services.appearance_service import AppearanceService

from ui.pages.settings.general_page import GeneralPage
from ui.pages.settings.appearance_page import AppearancePage


class SettingsDialog(QDialog):
    """
    Application settings dialog.
    """

    # -------------------------------------------------

    def __init__(
        self,
        settings: SettingsService,
        appearance_service: AppearanceService,
        parent=None,
    ) -> None:

        super().__init__(parent)

        self.settings = settings

        self.appearance_service = appearance_service

        self.setWindowTitle(
            "Settings"
        )

        self.resize(
            700,
            500,
        )

        self._create_widgets()

        self._build_ui()

        self._connect_signals()

        self._load_pages()

    # =================================================
    # UI
    # =================================================

    def _create_widgets(self) -> None:

        self.pages = QTabWidget()
    
        self.general_page = GeneralPage(
            self.settings
        )
    
        self.appearance_page = AppearancePage(
            self.settings,
            self.appearance_service,
        )
    
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok
            | QDialogButtonBox.Apply
            | QDialogButtonBox.Cancel
        )

    # -------------------------------------------------

    def _build_ui(self) -> None:

        layout = QVBoxLayout(
            self
        )

        self.pages.addTab(
            self.general_page,
            "General",
        )

        self.pages.addTab(
            self.appearance_page,
            "Appearance",
        )

        layout.addWidget(
            self.pages
        )

        layout.addWidget(
            self.buttons
        )

    # -------------------------------------------------

    def _connect_signals(self) -> None:

        self.buttons.accepted.connect(
            self._on_ok
        )

        self.buttons.rejected.connect(
            self._on_cancel
        )

        apply_button = self.buttons.button(
            QDialogButtonBox.Apply
        )

        if apply_button is not None:

            apply_button.clicked.connect(
                self._on_apply
            )

    # =================================================
    # Pages
    # =================================================

    def _load_pages(self) -> None:

        for index in range(
            self.pages.count()
        ):

            page = self.pages.widget(
                index
            )

            if hasattr(
                page,
                "load",
            ):

                page.load()

    # -------------------------------------------------

    def _validate_pages(self) -> bool:

        for index in range(
            self.pages.count()
        ):

            page = self.pages.widget(
                index
            )

            if hasattr(
                page,
                "validate",
            ):

                if not page.validate():

                    self.pages.setCurrentIndex(
                        index
                    )

                    return False

        return True

    # -------------------------------------------------

    def _apply_pages(self) -> None:

        for index in range(
            self.pages.count()
        ):

            page = self.pages.widget(
                index
            )

            if hasattr(
                page,
                "apply",
            ):

                page.apply()

        self.settings.sync()

        #
        # Apply appearance
        #

        self.appearance_service.apply()

    # =================================================
    # Buttons
    # =================================================

    def _on_apply(self) -> None:

        if not self._validate_pages():

            return

        self._apply_pages()

    # -------------------------------------------------

    def _on_ok(self) -> None:

        if not self._validate_pages():

            return

        self._apply_pages()

        self.accept()

    # -------------------------------------------------

    def _on_cancel(self) -> None:

        self._load_pages()

        self.reject()

