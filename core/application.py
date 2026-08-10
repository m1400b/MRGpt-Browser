"""
MRGpt Browser

Application
"""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication
from services.network_service import NetworkService
from services.service_container import ServiceContainer
from services.service_names import ServiceNames

from services.appearance_service import AppearanceService
from services.settings_service import SettingsService
from services.profile_service import ProfileService
from services.browser_service import BrowserService
from services.network_service import NetworkService

from core.profile.private_profile import PrivateProfile

from ui.windows.main_window import MainWindow


class Application:
    """
    Main application bootstrap.

    Responsibilities
    ----------------
    - Create QApplication
    - Register all application services
    - Create the main window
    - Start and shutdown the application
    """

    # -------------------------------------------------

    def __init__(self) -> None:

        self.qt = QApplication(sys.argv)

        self._configure_qt()

        self.services = ServiceContainer()

        self._register_services()
        
        self.services.resolve(
    ServiceNames.APPEARANCE
).apply()

        self.window = MainWindow(
            self.services
        )

    # -------------------------------------------------

    def _configure_qt(self) -> None:
        """
        Configure QApplication metadata.
        """

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
        """
        Create and register all application services.
        """
    
        #
        # Settings
        #
    
        settings_service = SettingsService()
    
        self.services.register(
            ServiceNames.SETTINGS,
            settings_service,
        )
    
        #
        # Profile
        #
    
        profile_service = ProfileService()
    
        profile_service.register(
            "Private",
            PrivateProfile(),
        )
    
        self.services.register(
            ServiceNames.PROFILE,
            profile_service,
        )
    
        #
        # Network
        #
    
        network_service = NetworkService()
    
        self.services.register(
            ServiceNames.NETWORK,
            network_service,
        )
    
        #
        # Browser
        #
    
        browser_service = BrowserService()
    
        self.services.register(
            ServiceNames.BROWSER,
            browser_service,
        )
    
        #
        # Appearance
        #
    
        appearance_service = AppearanceService(
            settings_service,
            self.qt,
        )
    
        self.services.register(
            ServiceNames.APPEARANCE,
            appearance_service,
        )
    
    

    # -------------------------------------------------

    def run(self) -> int:
        """
        Show main window and start Qt event loop.
        """

        self.window.show()

        return self.qt.exec()

    # -------------------------------------------------

    def shutdown(self) -> None:
        """
        Shutdown application services.
        """

        if hasattr(
            self.services,
            "shutdown",
        ):
            self.services.shutdown()

        else:
            self.services.clear()