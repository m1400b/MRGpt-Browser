"""
MRGpt Browser

Address Bar Widget
"""

from __future__ import annotations

from PySide6.QtCore import (
    Qt,
    Signal,
    QUrl
)


from PySide6.QtWidgets import (
    QLineEdit,
)


class AddressBar(QLineEdit):
    """
    Browser Address Bar

    نسخه اولیه
    - نمایش URL
    - دریافت URL
    - سیگنال Navigate
    """

    # ---------------------------------------------

    navigate_requested = Signal(str)

    # ---------------------------------------------

    def __init__(self, parent=None):

        super().__init__(parent)

        self._configure()

        self._connect_signals()

    # ---------------------------------------------

    def _configure(self):

        self.setPlaceholderText(
            "Search or enter address..."
        )

        self.setClearButtonEnabled(True)

        self.setMinimumHeight(34)

        self.setFrame(False)

        self.setStyleSheet("""

            QLineEdit{

                border:1px solid #C8C8C8;

                border-radius:17px;

                padding-left:12px;

                padding-right:12px;

                background:white;

                selection-background-color:#2A7FFF;

            }

            QLineEdit:focus{

                border:2px solid #2A7FFF;

            }

        """)

    # ---------------------------------------------

    def _connect_signals(self):

        self.returnPressed.connect(

            self._return_pressed

        )

    # ---------------------------------------------

    def _return_pressed(self):

        text = self.text().strip()

        if not text:

            return

        self.navigate_requested.emit(text)

    # ---------------------------------------------

    def set_url(
    self,
    url: str | QUrl
):

        if isinstance(url, QUrl):
            url = url.toString()

        self.setText(url)

    # ---------------------------------------------

    def url(self):

        """
        URL فعلی
        """

        return self.text().strip()

    # ---------------------------------------------

    def clear_url(self):

        """
        پاک کردن آدرس
        """

        self.clear()

    # ---------------------------------------------

    def select_all(self):

        """
        انتخاب کل متن
        """

        self.select_all()

    # ---------------------------------------------

    def focusInEvent(self, event):

        super().focusInEvent(event)

        self.selectAll()

    # ---------------------------------------------

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:

            self.clearFocus()

            return

        super().keyPressEvent(event)