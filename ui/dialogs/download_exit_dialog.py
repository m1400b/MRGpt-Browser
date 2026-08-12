"""
MRGpt Browser

Download Exit Dialog
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
)


class DownloadExitDialog(QDialog):
    """
    Warn the user before closing the browser
    while downloads are active.
    """

    def __init__(
        self,
        active_count: int,
        parent=None,
    ) -> None:

        super().__init__(parent)

        self.setWindowTitle(
            "Download in Progress"
        )

        self.setModal(
            True
        )

        # -------------------------------------------------
        # Message
        # -------------------------------------------------

        if active_count == 1:

            message = (
                "یک فایل در حال دانلود است.\n\n"
                "اگر مرورگر را ببندید، "
                "دانلود متوقف خواهد شد."
            )

        else:

            message = (
                f"{active_count} فایل در حال دانلود هستند.\n\n"
                "اگر مرورگر را ببندید، "
                "دانلودها متوقف خواهند شد."
            )

        label = QLabel(
            message
        )

        label.setWordWrap(
            True
        )

        # -------------------------------------------------
        # Buttons
        # -------------------------------------------------

        buttons = QDialogButtonBox()

        self.cancel_button = buttons.addButton(
            "Cancel",
            QDialogButtonBox.RejectRole,
        )

        self.exit_button = buttons.addButton(
            "Exit Anyway",
            QDialogButtonBox.AcceptRole,
        )

        buttons.rejected.connect(
            self.reject
        )

        buttons.accepted.connect(
            self.accept
        )

        # -------------------------------------------------
        # Layout
        # -------------------------------------------------

        layout = QVBoxLayout(
            self
        )

        layout.addWidget(
            label
        )

        layout.addWidget(
            buttons
        )