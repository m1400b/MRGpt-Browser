"""
MRGpt Browser

Browser Page
"""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtWebEngineCore import (
    QWebEnginePage,
    QWebEngineProfile,
    QWebEngineCertificateError,
)


class BrowserPage(QWebEnginePage):

    new_tab_requested = Signal(QUrl)

    new_window_requested = Signal(QWebEnginePage.WebWindowType)

    download_requested = Signal(QUrl)

    permission_requested = Signal(str)

    javascript_console = Signal(
        object,
    str,
    int,
    str
    )

    certificate_error = Signal(str)

    file_dialog_requested = Signal()

    close_requested = Signal()

    title_changed = Signal(str)

    icon_changed = Signal()


    def __init__(
        self,
        profile: QWebEngineProfile,
        parent: QObject | None = None
    ):

        super().__init__(
            profile,
            parent
        )

        self.titleChanged.connect(
            self.title_changed.emit
        )

        self.iconChanged.connect(
            lambda _: self.icon_changed.emit()
        )


    def createWindow(
    self,
    window_type
):

        page = BrowserPage(
            self.profile()
        )

        page.urlChanged.connect(
            lambda url:
            self.new_tab_requested.emit(url)
        )

        return page
    
    
    def certificateError(
        self,
        error: QWebEngineCertificateError
    ):

        self.certificate_error.emit(
            error.description()
        )

        return False


    def javaScriptConsoleMessage(
        self,
        level,
        message,
        line_number,
        source_id
    ):

        level_value = getattr(
            level,
            "value",
            level
        )

        self.javascript_console.emit(
            level_value,
            message,
            line_number,
            source_id
        )


    def featurePermissionRequested(
        self,
        security_origin,
        feature
    ):

        self.permission_requested.emit(
            security_origin.toString()
        )

        self.setFeaturePermission(
            security_origin,
            feature,
            QWebEnginePage.PermissionDeniedByUser
        )


    def chooseFiles(
        self,
        mode,
        old_files,
        accepted_mime_types
    ):

        self.file_dialog_requested.emit()

        return []


    def trigger_download(
        self,
        url: QUrl
    ):

        self.download_requested.emit(url)


    def create_new_tab(
        self,
        url: QUrl
    ):

        self.new_tab_requested.emit(url)
    
    def open_url(
    self,
    url: QUrl
):

        self.load(url)
        
    def current_url(self):

        return self.url()
    
    def profile_object(self):

        return self.profile()