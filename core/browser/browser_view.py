"""
MRGpt Browser

Browser View
"""

from __future__ import annotations

from PySide6.QtCore import (
    Qt,
    QUrl,
    Signal,
)

from PySide6.QtGui import QAction

from PySide6.QtWidgets import QMenu

from PySide6.QtWebEngineWidgets import QWebEngineView

from core.browser.browser_page import BrowserPage


class BrowserView(QWebEngineView):

    # -------------------------------------------------
    # Signals
    # -------------------------------------------------

    close_requested = Signal()

    title_changed = Signal(str)

    url_changed = Signal(QUrl)

    icon_changed = Signal()

    load_started = Signal()

    load_finished = Signal(bool)

    load_progress = Signal(int)

    new_tab_requested = Signal(QUrl)

    download_requested = Signal(object)

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------

    def __init__(
        self,
        profile,
        parent=None,
    ):

        super().__init__(parent)

        # ---------------------------------------------
        # Normalize BrowserProfile
        # ---------------------------------------------

        if hasattr(
            profile,
            "qt_profile",
        ):

            profile = profile.qt_profile

        # ---------------------------------------------
        # Create BrowserPage
        # ---------------------------------------------

        self.page_object = BrowserPage(
            profile,
            self,
        )

        self.setPage(
            self.page_object
        )

        print(
            "🔥 BROWSER VIEW PROFILE:",
            self.page().profile(),
        )

        print(
            "🔥 BROWSER VIEW PAGE:",
            self.page(),
        )

        # ---------------------------------------------
        # Shutdown state
        # ---------------------------------------------

        self._shutdown_started = False

        # ---------------------------------------------
        # Signals
        # ---------------------------------------------

        self._connect_signals()

    # =================================================
    # Signals
    # =================================================

    def _connect_signals(self):

        self.titleChanged.connect(
            self.title_changed.emit
        )

        self.urlChanged.connect(
            self.url_changed.emit
        )

        self.loadStarted.connect(
            self.load_started.emit
        )

        self.loadFinished.connect(
            self.load_finished.emit
        )

        self.loadProgress.connect(
            self.load_progress.emit
        )

        self.page_object.new_tab_requested.connect(
            self.new_tab_requested.emit
        )

        self.page_object.download_requested.connect(
            self.download_requested.emit
        )

        self.page_object.icon_changed.connect(
            self.icon_changed.emit
        )

        self.page_object.close_requested.connect(
            self.close_requested.emit
        )

    # =================================================
    # Navigation
    # =================================================

    def open_url(
        self,
        url,
    ):

        if isinstance(
            url,
            str,
        ):

            url = QUrl(url)

        self.load(url)

    # -------------------------------------------------

    def current_url(self):

        return self.url()

    # -------------------------------------------------

    def current_title(self):

        return self.title()

    # =================================================
    # Zoom
    # =================================================

    def zoom_in(self):

        self.setZoomFactor(
            self.zoomFactor() + 0.1
        )

    # -------------------------------------------------

    def zoom_out(self):

        self.setZoomFactor(
            max(
                0.25,
                self.zoomFactor() - 0.1,
            )
        )

    # -------------------------------------------------

    def reset_zoom(self):

        self.setZoomFactor(
            1.0
        )

    # =================================================
    # Context Menu
    # =================================================

    def contextMenuEvent(
        self,
        event,
    ):

        request = (
            self.lastContextMenuRequest()
        )

        if request is None:

            return super().contextMenuEvent(
                event
            )

        menu = QMenu(self)

        link = request.linkUrl()

        if link.isValid():

            action = QAction(
                "Open Link in New Tab",
                self,
            )

            action.triggered.connect(
                lambda:
                self.page_object.create_new_tab(
                    link
                )
            )

            menu.addAction(
                action
            )

        image = request.mediaUrl()

        if image.isValid():

            menu.addSeparator()

            image_action = QAction(
                "Open Image in New Tab",
                self,
            )

            image_action.triggered.connect(
                lambda:
                self.page_object.create_new_tab(
                    image
                )
            )

            menu.addAction(
                image_action
            )

        menu.addSeparator()

        standard_menu = (
            self.createStandardContextMenu()
        )

        menu.addActions(
            standard_menu.actions()
        )

        menu.exec(
            event.globalPos()
        )

    # =================================================
    # Wheel / Zoom
    # =================================================

    def wheelEvent(
        self,
        event,
    ):

        if (
            event.modifiers()
            & Qt.ControlModifier
        ):

            if event.angleDelta().y() > 0:

                self.zoom_in()

            else:

                self.zoom_out()

            event.accept()

            return

        super().wheelEvent(
            event
        )

    # =================================================
    # Navigation Actions
    # =================================================

    def back(self):

        self.page().triggerAction(
            self.page().WebAction.Back
        )

    # -------------------------------------------------

    def forward(self):

        self.page().triggerAction(
            self.page().WebAction.Forward
        )

    # -------------------------------------------------

    def reload(self):

        self.page().triggerAction(
            self.page().WebAction.Reload
        )

    # -------------------------------------------------

    def stop(self):

        self.page().triggerAction(
            self.page().WebAction.Stop
        )

    # =================================================
    # Shutdown
    # =================================================

    def shutdown(self) -> None:
        """
        Safely shutdown the WebEngine view.

        BrowserPage is owned by this BrowserView.
        The page is detached before it is scheduled
        for deletion.
        """

        if self._shutdown_started:

            return

        self._shutdown_started = True

        # ---------------------------------------------
        # Stop loading
        # ---------------------------------------------

        try:

            self.stop()

        except (
            RuntimeError,
            AttributeError,
        ):

            pass

        # ---------------------------------------------
        # Disconnect page signals
        # ---------------------------------------------

        page = self.page_object

        if page is not None:

            try:
                page.new_tab_requested.disconnect(
                    self.new_tab_requested.emit
                )

            except (
                RuntimeError,
                TypeError,
            ):

                pass

            try:
                page.download_requested.disconnect(
                    self.download_requested.emit
                )

            except (
                RuntimeError,
                TypeError,
            ):

                pass

            try:
                page.icon_changed.disconnect(
                    self.icon_changed.emit
                )

            except (
                RuntimeError,
                TypeError,
            ):

                pass

            try:
                page.close_requested.disconnect(
                    self.close_requested.emit
                )

            except (
                RuntimeError,
                TypeError,
            ):

                pass

        # ---------------------------------------------
        # Detach page from QWebEngineView
        # ---------------------------------------------

        try:

            self.setPage(
                None
            )

        except (
            RuntimeError,
            TypeError,
        ):

            pass

        # ---------------------------------------------
        # Schedule BrowserPage deletion
        # ---------------------------------------------

        if page is not None:

            try:

                page.deleteLater()

            except RuntimeError:

                pass

        # ---------------------------------------------
        # Do NOT destroy the profile here.
        #
        # ProfileService / Application owns it.
        # ---------------------------------------------