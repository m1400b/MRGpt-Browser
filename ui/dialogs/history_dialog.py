"""
MRGpt Browser

History Dialog
"""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QLabel,
    QAbstractItemView,
)

from services.history_service import HistoryService


class HistoryDialog(QDialog):
    """
    Display, search and manage browsing history.
    """

    def __init__(
        self,
        history_service: HistoryService,
        parent=None,
    ) -> None:

        super().__init__(parent)

        self.history_service = history_service

        self._setup_window()

        self._create_widgets()

        self._build_ui()

        self._connect_signals()

        self.refresh()

    # =================================================
    # Window
    # =================================================

    def _setup_window(self) -> None:

        self.setWindowTitle(
            "سابقه مرور"
        )

        self.resize(
            950,
            600,
        )

        self.setMinimumSize(
            750,
            450,
        )

        self.setLayoutDirection(
            Qt.RightToLeft
        )

    # =================================================
    # Widgets
    # =================================================

    def _create_widgets(self) -> None:

        self.title_label = QLabel(
            "سابقه مرورگر"
        )

        self.title_label.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            """
        )

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "جست‌وجو در عنوان یا آدرس صفحات..."
        )

        self.search_input.setClearButtonEnabled(
            True
        )

        self.refresh_button = QPushButton(
            "به‌روزرسانی"
        )

        self.delete_button = QPushButton(
            "حذف مورد انتخاب‌شده"
        )

        self.delete_button.setEnabled(
            False
        )

        self.close_button = QPushButton(
            "بستن"
        )

        self.count_label = QLabel()

        # ---------------------------------------------
        # History Table
        # ---------------------------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(
            4
        )

        self.table.setHorizontalHeaderLabels(
            [
                "عنوان صفحه",
                "آدرس",
                "آخرین بازدید",
                "تعداد بازدید",
            ]
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setWordWrap(
            False
        )

        self.table.verticalHeader().setVisible(
            False
        )

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.Stretch,
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.Stretch,
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents,
        )

    # =================================================
    # Layout
    # =================================================

    def _build_ui(self) -> None:

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        layout.setSpacing(
            14
        )

        # ---------------------------------------------
        # Title
        # ---------------------------------------------

        layout.addWidget(
            self.title_label
        )

        # ---------------------------------------------
        # Search
        # ---------------------------------------------

        search_layout = QHBoxLayout()

        search_layout.addWidget(
            self.search_input
        )

        search_layout.addWidget(
            self.refresh_button
        )

        layout.addLayout(
            search_layout
        )

        # ---------------------------------------------
        # Table
        # ---------------------------------------------

        layout.addWidget(
            self.table
        )

        # ---------------------------------------------
        # Footer
        # ---------------------------------------------

        footer_layout = QHBoxLayout()

        footer_layout.addWidget(
            self.count_label
        )

        footer_layout.addStretch()

        footer_layout.addWidget(
            self.delete_button
        )

        footer_layout.addWidget(
            self.close_button
        )

        layout.addLayout(
            footer_layout
        )

    # =================================================
    # Signals
    # =================================================

    def _connect_signals(self) -> None:

        self.search_input.textChanged.connect(
            self.refresh
        )

        self.refresh_button.clicked.connect(
            self.refresh
        )

        self.table.itemSelectionChanged.connect(
            self._update_buttons
        )

        self.delete_button.clicked.connect(
            self._delete_selected
        )

        self.close_button.clicked.connect(
            self.accept
        )

    # =================================================
    # History
    # =================================================

    def refresh(self, *args) -> None:

        keyword = self.search_input.text().strip()

        if keyword:

            items = self.history_service.search(
                keyword
            )

        else:

            items = self.history_service.all()

        # ---------------------------------------------
        # Sort by last visit
        # ---------------------------------------------

        items = sorted(
            items,
            key=lambda item: self._datetime_value(
                item.visit_time
            ),
            reverse=True,
        )

        # ---------------------------------------------
        # Populate table
        # ---------------------------------------------

        self.table.setSortingEnabled(
            False
        )

        self.table.setRowCount(
            len(items)
        )

        for row, item in enumerate(items):

            # Title
            title_item = QTableWidgetItem(
                item.title or item.url
            )

            # Keep database ID with the row.
            title_item.setData(
                Qt.UserRole,
                item.id,
            )

            # URL
            url_item = QTableWidgetItem(
                item.url
            )

            url_item.setToolTip(
                item.url
            )

            # Visit time
            time_item = QTableWidgetItem(
                self._format_datetime(
                    item.visit_time
                )
            )

            # Visit count
            count_item = QTableWidgetItem(
                str(item.visit_count)
            )

            count_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row,
                0,
                title_item,
            )

            self.table.setItem(
                row,
                1,
                url_item,
            )

            self.table.setItem(
                row,
                2,
                time_item,
            )

            self.table.setItem(
                row,
                3,
                count_item,
            )

        # ---------------------------------------------
        # Update footer
        # ---------------------------------------------

        self.table.clearSelection()

        self._update_buttons()

        total = self.history_service.count()

        if keyword:

            self.count_label.setText(
                f"نتایج جست‌وجو: {len(items)} | "
                f"کل صفحات ذخیره‌شده: {total}"
            )

        else:

            self.count_label.setText(
                f"تعداد صفحات ذخیره‌شده: {total}"
            )

    # =================================================
    # Date Helpers
    # =================================================

    @staticmethod
    def _datetime_value(value) -> datetime:

        if isinstance(value, datetime):

            return value

        if isinstance(value, str):

            try:

                return datetime.fromisoformat(
                    value
                )

            except ValueError:

                pass

        return datetime.min

    # -------------------------------------------------

    @classmethod
    def _format_datetime(cls, value) -> str:

        date = cls._datetime_value(
            value
        )

        if date == datetime.min:

            return "نامشخص"

        return date.strftime(
            "%Y/%m/%d - %H:%M:%S"
        )

    # =================================================
    # Selection
    # =================================================

    def _selected_history_id(self) -> int | None:

        row = self.table.currentRow()

        if row < 0:

            return None

        item = self.table.item(
            row,
            0,
        )

        if item is None:

            return None

        history_id = item.data(
            Qt.UserRole
        )

        if history_id is None:

            return None

        return int(history_id)

    # -------------------------------------------------

    def _update_buttons(self) -> None:

        self.delete_button.setEnabled(
            self._selected_history_id() is not None
        )

    # =================================================
    # Delete
    # =================================================

    def _delete_selected(self) -> None:

        history_id = self._selected_history_id()

        if history_id is None:

            return

        result = QMessageBox.question(
            self,
            "حذف سابقه مرور",
            "آیا از حذف بازدید انتخاب‌شده اطمینان دارید؟",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if result != QMessageBox.Yes:

            return

        try:

            self.history_service.remove(
                history_id
            )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "خطا در حذف سابقه",
                f"حذف سابقه انجام نشد:\n{exc}",
            )

            return

        self.refresh()