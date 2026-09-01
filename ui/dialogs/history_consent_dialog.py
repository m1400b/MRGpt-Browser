"""
MRGpt Browser

History Consent Dialog
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
)


class HistoryConsentDialog(QDialog):
    """
    Ask the user whether browsing history should be saved.

    The dialog is intentionally responsible only for user interaction.
    Persistence is handled by the application/settings layer.
    """

    def __init__(
        self,
        save_history: bool = True,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self._save_history = bool(save_history)

        self._setup_window()
        self._build_ui()

    # =========================================================
    # Setup
    # =========================================================

    def _setup_window(self) -> None:
        self.setWindowTitle("حریم خصوصی و سابقه مرور")
        self.setModal(True)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setMinimumWidth(460)

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        title = QLabel("آیا می‌خواهید سابقه مرور شما ذخیره شود؟")
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignRight)
        title.setStyleSheet(
            "font-size: 18px; font-weight: 600;"
        )

        description = QLabel(
            "در صورت فعال بودن این گزینه، نشانی صفحات بازدیدشده "
            "در سابقه مرورگر ذخیره می‌شود و بعداً می‌توانید آن را "
            "از بخش تنظیمات مدیریت یا حذف کنید."
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignRight)
        description.setStyleSheet("font-size: 13px; line-height: 1.5;")

        self._remember_checkbox = QCheckBox(
            "این انتخاب را به خاطر بسپار و دوباره سؤال نکن"
        )
        self._remember_checkbox.setLayoutDirection(Qt.RightToLeft)
        self._remember_checkbox.setChecked(False)

        buttons = QDialogButtonBox()

        save_button = buttons.addButton(
            "ذخیره سابقه",
            QDialogButtonBox.AcceptRole,
        )
        disable_button = buttons.addButton(
            "ذخیره نکن",
            QDialogButtonBox.DestructiveRole,
        )

        save_button.clicked.connect(
            lambda: self._finish(True)
        )
        disable_button.clicked.connect(
            lambda: self._finish(False)
        )

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(4)
        layout.addWidget(self._remember_checkbox)
        layout.addSpacing(8)
        layout.addWidget(buttons)

    # =========================================================
    # Result
    # =========================================================

    def _finish(self, save_history: bool) -> None:
        self._save_history = bool(save_history)
        self.accept()

    @property
    def save_history(self) -> bool:
        """Return the user's selected history preference."""
        return self._save_history

    @property
    def remember_choice(self) -> bool:
        """Return whether the user asked not to be prompted again."""
        return self._remember_checkbox.isChecked()
