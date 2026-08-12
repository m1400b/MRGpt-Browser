"""
MRGpt Browser

Main Window
"""

from __future__ import annotations

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QProgressBar,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtWidgets import QApplication
from services.service_container import ServiceContainer
from services.service_names import ServiceNames

from core.browser.browser import Browser

from ui.dialogs.settings_dialog import SettingsDialog
from ui.widgets.browser.browser_toolbar import BrowserToolbar
from ui.widgets.browser.page_loading_bar import LoadingBar


class MainWindow(QMainWindow):
    """
    Main application window.

    Responsibilities
    ----------------
    - Build UI
    - Connect widgets together
    - Forward user actions
    - Shutdown browser resources safely
    """

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------

    def __init__(
        self,
        services: ServiceContainer,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        # ---------------------------------------------
        # Services
        # ---------------------------------------------

        self.services = services

        self.settings_service = services.resolve(
            ServiceNames.SETTINGS
        )

        self.appearance_service = services.resolve(
            ServiceNames.APPEARANCE
        )

        self.profile_service = services.resolve(
            ServiceNames.PROFILE
        )

        self.browser_service = services.resolve(
            ServiceNames.BROWSER
        )

        # ---------------------------------------------
        # Shutdown state
        # ---------------------------------------------

        self._shutdown_started = False

        # ---------------------------------------------
        # Window
        # ---------------------------------------------

        self.setWindowTitle(
            "MRGpt Browser"
        )

        self.resize(
            1500,
            900,
        )

        # ---------------------------------------------
        # Create Browser + Widgets
        # ---------------------------------------------

        self._create_browser()

        # ---------------------------------------------
        # Build UI
        # ---------------------------------------------

        self._build_ui()

        self._create_statusbar()

        self._connect_signals()

        # ---------------------------------------------
        # Initial Page
        # ---------------------------------------------

        self.browser.new_tab(
            QUrl(
                self.settings_service.home_page
            )
        )

    # =================================================
    # Browser / Widgets
    # =================================================

    def _create_browser(self) -> None:
        """
        Create browser facade and browser widgets.
        """

        self.browser = Browser(
            self.services
        )

        self.toolbar = BrowserToolbar()

        self.loading_bar = LoadingBar()

    # =================================================
    # UI
    # =================================================

    def _build_ui(self) -> None:

        container = QWidget()

        layout = QVBoxLayout(
            container
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(0)

        layout.addWidget(
            self.toolbar
        )

        layout.addWidget(
            self.loading_bar
        )

        layout.addWidget(
            self.browser,
            1,
        )

        self.setCentralWidget(
            container
        )

    # =================================================
    # Status Bar
    # =================================================

    def _create_statusbar(self) -> None:

        self.status = QStatusBar()

        self.setStatusBar(
            self.status
        )

        self.progress = QProgressBar()

        self.progress.setMaximumWidth(
            150
        )

        self.progress.hide()

        self.status.addPermanentWidget(
            self.progress
        )

        self.ssl_label = QLabel()

        self.status.addPermanentWidget(
            self.ssl_label
        )

    # =================================================
    # Signals
    # =================================================

    def _connect_signals(self) -> None:

        # ---------------------------------------------
        # Toolbar
        # ---------------------------------------------

        self.toolbar.back_requested.connect(
            self.browser.back
        )

        self.toolbar.forward_requested.connect(
            self.browser.forward
        )

        self.toolbar.reload_requested.connect(
            self.browser.reload
        )

        self.toolbar.new_tab_requested.connect(
            self.browser.new_tab
        )

        self.toolbar.home_requested.connect(
            self._go_home
        )

        self.toolbar.navigate_requested.connect(
            self.browser.navigate
        )

        self.toolbar.settings_requested.connect(
            self._open_settings
        )

        # ---------------------------------------------
        # Browser
        # ---------------------------------------------

        self.browser.title_changed.connect(
            self.setWindowTitle
        )

        self.browser.url_changed.connect(
            self.toolbar.set_url
        )

        self.browser.current_tab_changed.connect(
            self._update_navigation_state
        )

        self.browser.load_started.connect(
            self._load_started
        )

        self.browser.load_progress.connect(
            self._load_progress
        )

        self.browser.load_finished.connect(
            self._load_finished
        )

    # =================================================
    # Home
    # =================================================

    def _go_home(self) -> None:

        self.browser.navigate(
            self.settings_service.home_page
        )

    # =================================================
    # Navigation State
    # =================================================

    def _update_navigation_state(self) -> None:

        self.toolbar.set_navigation_state(
            self.browser.can_go_back(),
            self.browser.can_go_forward(),
        )

    # =================================================
    # Loading
    # =================================================

    def _load_started(self) -> None:

        self.progress.show()

        self.loading_bar.start()

        self.toolbar.set_loading(
            True
        )

    # -------------------------------------------------

    def _load_progress(
        self,
        value: int,
    ) -> None:

        self.progress.setValue(
            value
        )

        self.loading_bar.set_value(
            value
        )

    # -------------------------------------------------

    def _load_finished(
        self,
        ok: bool,
    ) -> None:

        self.progress.hide()

        self.loading_bar.finish()

        self.toolbar.set_loading(
            False
        )

    # =================================================
    # Keyboard
    # =================================================

    def keyPressEvent(
        self,
        event,
    ) -> None:

        if event.matches(
            QKeySequence.Refresh
        ):

            self.browser.reload()

            return

        super().keyPressEvent(
            event
        )

    # =================================================
    # Settings
    # =================================================

    def _open_settings(self) -> None:
        """
        Open application settings dialog.
        """

        dialog = SettingsDialog(
            self.settings_service,
            self.appearance_service,
            self,
        )

        dialog.exec()

    # =================================================
    # Shutdown
    # =================================================
    def closeEvent(
    self,
    event,
) -> None:
        """
        Close the main window and shutdown browser resources.
        """

        if self._shutdown_started:

            event.accept()

            return

        self._shutdown_started = True

        print(
            "🧹 MAIN WINDOW CLOSE EVENT"
        )

        # ---------------------------------------------
        # Shutdown Browser
        # ---------------------------------------------

        if self.browser is not None:

            self.browser.shutdown()

            print(
                "✅ BROWSER SHUTDOWN COMPLETED"
            )

        # ---------------------------------------------
        # Process deferred QObject deletion
        # ---------------------------------------------

        QApplication.processEvents()

        # ---------------------------------------------
        # Accept close
        # ---------------------------------------------

        event.accept()

        print(
            "🧹 MAIN WINDOW CLOSE EVENT FINISHED"
        )
    
