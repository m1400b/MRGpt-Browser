"""
MRGpt Browser

Tab Manager

Manage Browser Tabs
"""


from __future__ import annotations


from PySide6.QtCore import (
    QObject,
    Signal,
    QUrl
)


from PySide6.QtWidgets import (
    QTabWidget
)


from core.browser.browser_tab import BrowserTab

class TabManager(QObject):


    # ---------------------------------
    # Signals
    # ---------------------------------

    tab_created = Signal(
        BrowserTab
    )


    tab_closed = Signal(
        int
    )


    current_changed = Signal(
        int
    )


    title_changed = Signal(
        int,
        str
    )


    url_changed = Signal(
        int,
        QUrl
    )


    download_requested = Signal(
        QUrl
    )


    # ---------------------------------

    def __init__(
        self,
        tab_widget: QTabWidget,
        profile,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.tab_widget = tab_widget

        self.profile = profile
        
        self.tab_widget.setTabsClosable(True)

        self.tab_widget.setMovable(True)

        self.tab_widget.setDocumentMode(True)

        self.tab_widget.setUsesScrollButtons(True)


        self._connect_widget()



    # ---------------------------------

    def _connect_widget(self):

        self.tab_widget.currentChanged.connect(
            self.current_changed.emit
        )
        
        self.tab_widget.tabCloseRequested.connect(
    self.close_tab
)



    # ---------------------------------

    def create_tab(
        self,
        url=None
    ):

        """
        Create new browser tab
        """


        tab = BrowserTab(
            self.profile
        )


        index = self.tab_widget.addTab(
            tab,
            "New Tab"
        )


        self._connect_tab(
            tab
        )


        self.tab_widget.setCurrentIndex(
            index
        )


        self.tab_created.emit(
            tab
        )


        if url is not None:

            if isinstance(url, str):
                url = QUrl(url)
        
            tab.load(url)


        return tab



    # ---------------------------------

    def _connect_tab(
        self,
        tab: BrowserTab
    ):


        tab.title_changed.connect(

            lambda title:

            self._update_title(
                tab,
                title
            )

        )


        tab.url_changed.connect(

            lambda url:

            self._update_url(
                tab,
                url
            )

        )


        tab.new_tab_requested.connect(

            self.create_tab

        )


        tab.download_requested.connect(

            self.download_requested.emit

        )



    # ---------------------------------

    def _tab_index(
        self,
        tab
    ):

        return self.tab_widget.indexOf(
            tab
        )



    # ---------------------------------

    def _update_title(
        self,
        tab,
        title
    ):

        index = self._tab_index(
            tab
        )


        if index < 0:
            return


        if not title:

            title = "New Tab"

        MAX_TAB_TITLE = 35

        self.tab_widget.setTabText(
    index,
    title[:MAX_TAB_TITLE]
)


        self.title_changed.emit(
            index,
            title
        )



    # ---------------------------------

    def _update_url(
        self,
        tab,
        url
    ):

        index = self._tab_index(
            tab
        )


        if index < 0:
            return


        self.url_changed.emit(
            index,
            url
        )



    # ---------------------------------

    def close_tab(
        self,
        index
    ):


        if index < 0:
            return


        if index >= self.tab_widget.count():
            return



        widget = self.tab_widget.widget(
            index
        )


        self.tab_widget.removeTab(
            index
        )


        if widget:

            widget.deleteLater()



        self.tab_closed.emit(
            index
        )



        if self.tab_widget.count() == 0:

            self.create_tab()



    # ---------------------------------

    def current_tab(self):


        widget = self.tab_widget.currentWidget()


        if isinstance(
            widget,
            BrowserTab
        ):

            return widget


        return None



    # ---------------------------------

    def current_index(self):

        return self.tab_widget.currentIndex()



    # ---------------------------------

    def count(self):

        return self.tab_widget.count()



    # ---------------------------------

    def close_current_tab(self):

        self.close_tab(
            self.current_index()
        )



    # ---------------------------------

    def next_tab(self):


        count = self.count()


        if count <= 1:
            return


        index = (
            self.current_index()
            + 1
        )


        if index >= count:

            index = 0



        self.tab_widget.setCurrentIndex(
            index
        )



    # ---------------------------------

    def previous_tab(self):


        count = self.count()


        if count <= 1:
            return


        index = (
            self.current_index()
            - 1
        )


        if index < 0:

            index = count - 1



        self.tab_widget.setCurrentIndex(
            index
        )
    
    @property
    def current(self):

        return self.current_tab()
    
    @property
    def current_view(self):

        tab = self.current_tab()

        return None if tab is None else tab.view
    
    @property
    def current_page(self):

        tab = self.current_tab()

        return None if tab is None else tab.page
    
    @property
    def current_url(self):

        tab = self.current_tab()

        return None if tab is None else tab.url
    
    def tab(self, index):

        widget = self.tab_widget.widget(index)

        if isinstance(widget, BrowserTab):
            return widget

        return None
    
    def duplicate_tab(self, index):

        tab = self.tab(index)

        if tab is None:
            return

        self.create_tab(tab.url)
    
    def reopen_last_closed(self):

        pass
    
    def pin_tab(self, index):

        pass
    
    def move_tab(
    self,
    from_index,
    to_index
):

        self.tab_widget.tabBar().moveTab(
            from_index,
            to_index
        )