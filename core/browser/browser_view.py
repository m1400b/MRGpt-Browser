"""
MRGpt Browser

Browser View
"""

from __future__ import annotations

from PySide6.QtCore import (
    Qt,
    QUrl,
    Signal
)

from PySide6.QtGui import QAction

from PySide6.QtWidgets import QMenu

from PySide6.QtWebEngineWidgets import QWebEngineView


from core.browser.browser_page import BrowserPage



class BrowserView(QWebEngineView):

    close_requested = Signal()
    
    title_changed = Signal(str)

    url_changed = Signal(QUrl)

    icon_changed = Signal()

    load_started = Signal()

    load_finished = Signal(bool)

    load_progress = Signal(int)

    new_tab_requested = Signal(QUrl)

    download_requested = Signal(QUrl)



    def __init__(
        self,
        profile,
        parent=None
    ):

        super().__init__(parent)


        self.page_object = BrowserPage(
            profile,
            self
        )


        self.setPage(
            self.page_object
        )


        self._connect_signals()



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



    def open_url(self,url):

        if isinstance(url,str):
            url = QUrl(url)

        self.load(url)



    def current_url(self):

        return self.url()



    def current_title(self):

        return self.title()



    def zoom_in(self):

        self.setZoomFactor(
            self.zoomFactor()+0.1
        )


    def zoom_out(self):

        self.setZoomFactor(
            max(
                0.25,
                self.zoomFactor()-0.1
            )
        )


    def reset_zoom(self):

        self.setZoomFactor(1)



    def contextMenuEvent(self,event):

        menu = QMenu(self)


        open_tab = QAction(
            "Open link in new tab",
            self
        )
        
        request = self.lastContextMenuRequest()

        if request is None:
            return super().contextMenuEvent(event)
        
        link = request.linkUrl()

        if link.isValid():
        
            action = QAction(
                "Open Link in New Tab",
                self
            )

            action.triggered.connect(
                lambda:
                self.page_object.create_new_tab(link)
            )

            menu.addAction(action)
            
        image = request.mediaUrl()

        if image.isValid():
        
            menu.addSeparator()

            image_action = QAction(
                "Open Image in New Tab",
                self
            )

            image_action.triggered.connect(
                lambda:
                self.page_object.create_new_tab(image)
            )

            menu.addAction(image_action)


        menu.addAction(open_tab)


        menu.addActions(
            self.createStandardContextMenu().actions()
        )


        menu.exec(
            event.globalPos()
        )
        
    def wheelEvent(self, event):

        if event.modifiers() & Qt.ControlModifier:

            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()

            event.accept()
            return

        super().wheelEvent(event)
    
    def back(self):
        self.page().triggerAction(
            self.page().WebAction.Back
        )
    
    
    def forward(self):
        self.page().triggerAction(
            self.page().WebAction.Forward
        )
    
    
    def reload(self):
        self.page().triggerAction(
            self.page().WebAction.Reload
        )
    
    
    def stop(self):
        self.page().triggerAction(
            self.page().WebAction.Stop
        )