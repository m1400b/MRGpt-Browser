"""
MRGpt Browser

Browser Page
"""

from __future__ import annotations

from PySide6.QtCore import (
    QObject,
    Signal,
    QUrl,
)

from PySide6.QtWebEngineCore import (
    QWebEnginePage,
    QWebEngineProfile,
    QWebEngineCertificateError,
)


class BrowserPage(QWebEnginePage):

    # -------------------------------------------------
    # Signals
    # -------------------------------------------------

    new_tab_requested = Signal(QUrl)

    new_window_requested = Signal(
        QWebEnginePage.WebWindowType
    )

    download_requested = Signal(object)

    permission_requested = Signal(str)

    javascript_console = Signal(
        object,
        str,
        int,
        str,
    )

    certificate_error = Signal(str)

    file_dialog_requested = Signal()

    close_requested = Signal()

    title_changed = Signal(str)

    icon_changed = Signal()

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------

    def __init__(
        self,
        profile,
        parent: QObject | None = None,
    ) -> None:

        # ---------------------------------------------
        # IMPORTANT
        #
        # profile may be:
        #
        # BrowserProfile
        # OR
        #
        # QWebEngineProfile
        #
        # Always normalize it here.
        # ---------------------------------------------

        if hasattr(
            profile,
            "qt_profile",
        ):

            profile = profile.qt_profile

        if not isinstance(
            profile,
            QWebEngineProfile,
        ):

            raise TypeError(
                "BrowserPage requires "
                "BrowserProfile or QWebEngineProfile."
            )

        super().__init__(
            profile,
            parent,
        )

        # ---------------------------------------------
        # Debug
        # ---------------------------------------------

        print(
            "🔥 BROWSER PAGE PROFILE:",
            self.profile(),
        )

        print(
            "🔥 BROWSER PAGE OBJECT:",
            self,
        )

        # ---------------------------------------------
        # Page signals
        # ---------------------------------------------

        self.titleChanged.connect(
            self.title_changed.emit
        )

        self.iconChanged.connect(
            lambda _icon:
            self.icon_changed.emit()
        )

    # =================================================
    # Windows / Tabs
    # =================================================

    def createWindow(
        self,
        window_type:
        QWebEnginePage.WebWindowType,
    ):

        page = BrowserPage(
            self.profile()
        )

        page.urlChanged.connect(
            lambda url:
            self.new_tab_requested.emit(
                url
            )
        )

        self.new_window_requested.emit(
            window_type
        )

        return page

    # =================================================
    # Certificate
    # =================================================

    def certificateError(
        self,
        error: QWebEngineCertificateError,
    ) -> bool:

        self.certificate_error.emit(
            error.description()
        )

        return False

    # =================================================
    # JavaScript Console
    # =================================================

    def javaScriptConsoleMessage(
        self,
        level,
        message,
        line_number,
        source_id,
    ) -> None:

        level_value = getattr(
            level,
            "value",
            level,
        )

        self.javascript_console.emit(
            level_value,
            message,
            line_number,
            source_id,
        )

    # =================================================
    # Permissions
    # =================================================

    def featurePermissionRequested(
        self,
        security_origin,
        feature,
    ) -> None:

        self.permission_requested.emit(
            security_origin.toString()
        )

        self.setFeaturePermission(
            security_origin,
            feature,
            QWebEnginePage.PermissionDeniedByUser,
        )

    # =================================================
    # File Dialog
    # =================================================

    def chooseFiles(
        self,
        mode,
        old_files,
        accepted_mime_types,
    ):

        self.file_dialog_requested.emit()

        return []

    # =================================================
    # Compatibility
    # =================================================

    def trigger_download(
        self,
        url: QUrl,
    ) -> None:

        self.download_requested.emit(
            url
        )

    # -------------------------------------------------

    def create_new_tab(
        self,
        url: QUrl,
    ) -> None:

        self.new_tab_requested.emit(
            url
        )

    # -------------------------------------------------

    def open_url(
        self,
        url: QUrl,
    ) -> None:

        self.load(url)

    # -------------------------------------------------

    def current_url(self):

        return self.url()

    # -------------------------------------------------

    def profile_object(self):

        return self.profile()