"""
MRGpt Browser

History Settings Page
"""

from __future__ import annotations


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton,
    QMessageBox,
    QGroupBox,
)

from services.settings_service import SettingsService
from services.history_service import HistoryService
from ui.dialogs.history_dialog import HistoryDialog
from PySide6.QtCore import Qt, Signal

class HistoryPage(QWidget):
    """
    History settings and management.
    """
    open_url_requested = Signal(str)
    
    def __init__(
        self,
        settings: SettingsService,
        history_service: HistoryService,
        parent=None,
    ) -> None:

        super().__init__(parent)

        self.settings = settings
        self.history_service = history_service

        self._create_widgets()
        self._build_ui()
        self._connect_signals()

        self.load()

    # =================================================
    # Widgets
    # =================================================

    def _create_widgets(self) -> None:

        self.save_history_checkbox = QCheckBox(
            "ذخیره سابقه مرور"
        )

        self.ask_history_checkbox = QCheckBox(
            "هنگام اجرای مرورگر درباره ذخیره سابقه سؤال شود"
        )

        self.history_count_label = QLabel()

        self.clear_history_button = QPushButton(
            "پاک کردن تمام سابقه مرور"
        )
        
        self.view_history_button = QPushButton(
    "مشاهده تاریخچه"
)

    # =================================================
    # UI
    # =================================================

    def _build_ui(self) -> None:

        self.setLayoutDirection(
            Qt.RightToLeft
        )

        layout = QVBoxLayout(self)

        settings_group = QGroupBox(
            "تنظیمات سابقه مرور"
        )

        settings_layout = QVBoxLayout(
            settings_group
        )

        settings_layout.addWidget(
            self.save_history_checkbox
        )

        settings_layout.addWidget(
            self.ask_history_checkbox
        )

        layout.addWidget(
            settings_group
        )

        management_group = QGroupBox(
            "مدیریت سابقه مرور"
        )

        management_layout = QVBoxLayout(
            management_group
        )

        management_layout.addWidget(
            self.history_count_label
        )

        buttons_layout = QHBoxLayout()

        buttons_layout.addWidget(
    self.view_history_button
)
        
        buttons_layout.addWidget(
            self.clear_history_button
        )

        buttons_layout.addStretch()

        management_layout.addLayout(
            buttons_layout
        )

        layout.addWidget(
            management_group
        )

        layout.addStretch()

    # =================================================
    # Signals
    # =================================================

    def _connect_signals(self) -> None:

        self.clear_history_button.clicked.connect(
            self._clear_history
        )
        
        self.view_history_button.clicked.connect(
    self._show_history
)

    # =================================================
    # Settings Page API
    # =================================================

    def load(self) -> None:

        self.save_history_checkbox.setChecked(
            self.settings.save_history
        )

        self.ask_history_checkbox.setChecked(
            self.settings.ask_save_history
        )

        self._refresh_history_count()

    # -------------------------------------------------

    def validate(self) -> bool:

        return True

    # -------------------------------------------------

    def apply(self) -> None:

        self.settings.save_history = (
            self.save_history_checkbox.isChecked()
        )

        self.settings.ask_save_history = (
            self.ask_history_checkbox.isChecked()
        )

    # =================================================
    # History Management
    # =================================================

    def _refresh_history_count(self) -> None:

        count = self.history_service.count()

        self.history_count_label.setText(
            f"تعداد صفحات ذخیره‌شده: {count}"
        )

    # -------------------------------------------------

    def _clear_history(self) -> None:

        count = self.history_service.count()

        if count == 0:

            QMessageBox.information(
                self,
                "سابقه مرور",
                "سابقه‌ای برای حذف وجود ندارد.",
            )

            return

        result = QMessageBox.question(
            self,
            "پاک کردن سابقه مرور",
            (
                f"آیا از حذف تمام {count} رکورد سابقه مرور "
                "اطمینان دارید؟\n\n"
                "این عملیات قابل بازگشت نیست."
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if result != QMessageBox.Yes:
            return

        self.history_service.clear()

        self._refresh_history_count()

        QMessageBox.information(
            self,
            "سابقه مرور",
            "تمام سابقه مرور با موفقیت پاک شد.",
        )
        
    # =================================================
    # View History
    # =================================================
    def _show_history(self) -> None:

        dialog = HistoryDialog(
            self.history_service,
            self,
        )
    
        dialog.open_url_requested.connect(
            self.open_url_requested.emit
        )
    
        dialog.exec()
    
        self._refresh_history_count()