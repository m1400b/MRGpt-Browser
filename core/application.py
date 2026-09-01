"""
MRGpt Browser

Application
"""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from database.database_manager import DatabaseManager
from database.migrations import MigrationManager
from database.repository.download_repository import DownloadRepository
from services.appearance_service import AppearanceService
from services.browser_service import BrowserService
from services.download_manager import DownloadManager
from services.network_service import NetworkService
from services.profile_service import ProfileService
from services.service_container import ServiceContainer
from services.service_names import ServiceNames
from services.settings_service import SettingsService

from core.profile.private_profile import PrivateProfile

from ui.dialogs.history_consent_dialog import HistoryConsentDialog
from ui.windows.main_window import MainWindow


class Application:
    """
    Main application bootstrap.

    Responsibilities
    ----------------
    - Create QApplication
    - Register all application services
    - Handle startup privacy consent
    - Create the main window
    - Start and shutdown the application
    """

    def __init__(self) -> None:
        self.qt = QApplication(sys.argv)

        self._configure_qt()

        self.services = ServiceContainer()

        self._register_services()

        self.services.resolve(
            ServiceNames.APPEARANCE
        ).apply()

        # -------------------------------------------------
        # Privacy consent must be resolved before the
        # browser window starts loading its first page.
        # -------------------------------------------------
        self._handle_history_consent()

        self.window = MainWindow(
            self.services
        )

    # -------------------------------------------------

    def _configure_qt(self) -> None:
        """Configure QApplication metadata."""

        self.qt.setApplicationName(
            "MRGpt Browser"
        )

        self.qt.setOrganizationName(
            "MRGpt"
        )

        self.qt.setApplicationVersion(
            "0.1.0"
        )

    # -------------------------------------------------

    def _register_services(self) -> None:
        # ---------------------------------------------
        # Settings
        # ---------------------------------------------

        settings_service = SettingsService()

        self.services.register(
            ServiceNames.SETTINGS,
            settings_service,
        )

        # ---------------------------------------------
        # Database
        # ---------------------------------------------

        database_path = (
            Path.home()
            / ".mrgpt"
            / "mrgpt.db"
        )

        database_manager = DatabaseManager(
            str(database_path)
        )

        connection = database_manager.connect()

        MigrationManager(
            connection
        ).migrate()

        download_repository = DownloadRepository(
            connection
        )

        # ---------------------------------------------
        # Profile
        # ---------------------------------------------

        profile_service = ProfileService()

        private_profile = PrivateProfile()

        profile_service.register(
            "Private",
            private_profile,
        )

        self.services.register(
            ServiceNames.PROFILE,
            profile_service,
        )

        # ---------------------------------------------
        # Downloads
        # ---------------------------------------------

        download_manager = DownloadManager(
            settings_service,
            download_repository,
        )

        self.services.register(
            ServiceNames.DOWNLOADS,
            download_manager,
        )

        private_profile.download_requested.connect(
            download_manager.handle_download
        )

        # ---------------------------------------------
        # Browser
        # ---------------------------------------------

        browser_service = BrowserService()

        self.services.register(
            ServiceNames.BROWSER,
            browser_service,
        )

        # ---------------------------------------------
        # Network
        # ---------------------------------------------

        network_service = NetworkService()

        self.services.register(
            ServiceNames.NETWORK,
            network_service,
        )

        # ---------------------------------------------
        # Appearance
        # ---------------------------------------------

        appearance_service = AppearanceService(
            settings_service,
            self.qt,
        )

        self.services.register(
            ServiceNames.APPEARANCE,
            appearance_service,
        )

    # -------------------------------------------------

    def _handle_history_consent(self) -> None:
        """
        Resolve the user's browsing-history preference.

        The dialog is shown only while the corresponding setting
        says that the user should be asked. The selected preference
        is always persisted. If the user checks "remember", the
        startup prompt is disabled for subsequent launches.
        """

        settings = self.services.resolve(
            ServiceNames.SETTINGS
        )

        if not settings.ask_save_history:
            return

        dialog = HistoryConsentDialog(
            save_history=settings.save_history,
        )

        result = dialog.exec()

        # If the dialog is closed through the window manager, keep
        # the current persisted preference and ask again next time.
        if result != HistoryConsentDialog.Accepted:
            return

        settings.save_history = dialog.save_history

        if dialog.remember_choice:
            settings.ask_save_history = False
        else:
            settings.ask_save_history = True

        settings.sync()

        print(
            "🔐 HISTORY CONSENT:",
            "ENABLED" if settings.save_history else "DISABLED",
            "| ASK AGAIN:",
            settings.ask_save_history,
        )

    # -------------------------------------------------

    def run(self) -> int:
        """Show main window and start Qt event loop."""

        self.window.show()

        return self.qt.exec()

    # -------------------------------------------------

    def shutdown(self) -> None:
        """
        Shutdown application safely.

        Browser resources are released before profiles.
        """

        print(
            "🧹 APPLICATION SHUTDOWN STARTED"
        )

        # ---------------------------------------------
        # 1. Shutdown Browser
        # ---------------------------------------------

        if self.window is not None:
            if (
                hasattr(self.window, "browser")
                and self.window.browser is not None
            ):
                self.window.browser.shutdown()

                print(
                    "✅ BROWSER RESOURCES RELEASED"
                )

        # ---------------------------------------------
        # 2. Process deferred WebEngine deletions
        # ---------------------------------------------

        QApplication.processEvents()

        # ---------------------------------------------
        # 3. Close Main Window
        # ---------------------------------------------

        if self.window is not None:
            self.window.close()

            QApplication.processEvents()

            self.window.deleteLater()

            self.window = None

            QApplication.processEvents()

        # ---------------------------------------------
        # 4. Shutdown Services
        # ---------------------------------------------

        self.services.shutdown()

        print(
            "✅ APPLICATION SHUTDOWN FINISHED"
        )
