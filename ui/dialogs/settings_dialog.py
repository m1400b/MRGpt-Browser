"""
MRGpt Browser

Settings Dialog
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)
from services.settings_service import SettingsService
from ui.pages.settings.general_page import GeneralPage
from ui.pages.settings.base_settings_page import BaseSettingsPage

class SettingsDialog(QDialog):
    """
    Main Settings Dialog.

    Container for all settings pages.
    """

    # -------------------------------------------------

    def __init__(
    self,
    settings: SettingsService,
    parent=None,
) -> None:

        super().__init__(parent)
        self.settings = settings

        self.setWindowTitle(
            "Settings"
        )

        self.resize(
            850,
            600,
        )

        self._create_widgets()

        self._build_ui()

        self._connect()

        self._load_pages()

    # -------------------------------------------------

    def _create_widgets(self) -> None:

        self.category_list = QListWidget()

        self.category_list.setFixedWidth(
            180
        )

        self.pages = QStackedWidget()

        self.ok_button = QPushButton(
            "OK"
        )

        self.apply_button = QPushButton(
            "Apply"
        )

        self.cancel_button = QPushButton(
            "Cancel"
        )

    # -------------------------------------------------

    def _build_ui(self) -> None:

        main_layout = QVBoxLayout(
            self
        )

        content_layout = QHBoxLayout()

        content_layout.addWidget(
            self.category_list
        )

        content_layout.addWidget(
            self.pages,
            1
        )

        buttons_layout = QHBoxLayout()

        buttons_layout.addStretch()

        buttons_layout.addWidget(
            self.cancel_button
        )

        buttons_layout.addWidget(
            self.apply_button
        )

        buttons_layout.addWidget(
            self.ok_button
        )

        main_layout.addLayout(
            content_layout,
            1
        )

        main_layout.addLayout(
            buttons_layout
        )

    # -------------------------------------------------

    def _connect(self) -> None:

        self.category_list.currentRowChanged.connect(
            self.pages.setCurrentIndex
        )

        self.cancel_button.clicked.connect(
            self.reject
        )

        self.ok_button.clicked.connect(
            self._accept
        )

        self.apply_button.clicked.connect(
            self.apply
        )

    # -------------------------------------------------

    def _load_pages(self) -> None:

        self.add_page(

            "General",

            GeneralPage(
                self.settings
            )

        )

        self.category_list.setCurrentRow(0)

    # -------------------------------------------------

    def add_page(
        self,
        title: str,
        widget: QWidget,
    ) -> None:

        item = QListWidgetItem(
            title
        )

        self.category_list.addItem(
            item
        )

        self.pages.addWidget(
            widget
        )

    # -------------------------------------------------

    def save_settings(self) -> None:

    #
    # Validate
    #

        for index in range(self.pages.count()):
        
            page = self.pages.widget(index)
    
            if isinstance(page, BaseSettingsPage):
            
                if not page.validate():
                
                    return
    
        #
        # Save
        #
    
        for index in range(self.pages.count()):
        
            page = self.pages.widget(index)
    
            if isinstance(page, BaseSettingsPage):
            
                page.save_settings()
    
        #
        # Flush to disk
        #
    
        self.settings.sync()

    # -------------------------------------------------

    def _accept(self) -> None:

        self.apply()

        self.accept()