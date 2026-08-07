"""
MRGpt Browser

Loading Bar
"""

from __future__ import annotations

from PySide6.QtCore import (
    Property,
    QPropertyAnimation,
    QEasingCurve,
    QRect,
)

from PySide6.QtWidgets import QWidget

from PySide6.QtCore import Qt

class LoadingBar(QWidget):
    """
    Chrome Style Loading Bar
    """

    def __init__(self, parent=None) -> None:

        super().__init__(parent)

        self._progress = 0

        self.setFixedHeight(3)

        self.hide()

        self.setAttribute(
    Qt.WA_TransparentForMouseEvents
)

        self.animation = QPropertyAnimation(
            self,
            b"progress",
            self,
        )

        self.animation.setDuration(120)

        self.animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

    # -------------------------------------------------

    def getProgress(self) -> int:

        return self._progress

    # -------------------------------------------------

    def setProgress(
        self,
        value: int,
    ) -> None:

        self._progress = value

        self.update()

    # -------------------------------------------------

    progress = Property(
        int,
        getProgress,
        setProgress,
    )

    # -------------------------------------------------

    def start(self) -> None:

        self.show()

        self.setProgress(0)

    # -------------------------------------------------

    def finish(self) -> None:

        self.setProgress(100)

        self.hide()

    # -------------------------------------------------

    def set_value(
        self,
        value: int,
    ) -> None:

        self.animation.stop()

        self.animation.setStartValue(
            self._progress
        )

        self.animation.setEndValue(
            value
        )

        self.animation.start()

    # -------------------------------------------------

    def paintEvent(self, event):

        from PySide6.QtGui import (
            QColor,
            QPainter,
        )

        painter = QPainter(self)

        width = int(
            self.width() * self._progress / 100
        )

        painter.fillRect(
            QRect(
                0,
                0,
                width,
                self.height(),
            ),
            QColor("#2A7FFF"),
        )