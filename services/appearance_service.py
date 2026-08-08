"""
MRGpt Browser

Appearance Service
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from services.settings_service import SettingsService
from core.settings.settings_keys import SettingsKeys


class AppearanceService:
    """
    Application appearance service.

    این کلاس مسئول اعمال تنظیمات ظاهری
    برنامه است.

    ذخیره تنظیمات توسط SettingsService
    انجام می‌شود.
    """

    # -------------------------------------------------

    def __init__(
        self,
        settings_service: SettingsService,
        application: QApplication,
    ) -> None:

        self.settings = settings_service

        self.application = application

    # =================================================
    # Apply
    # =================================================

    def apply(self) -> None:
        """
        Apply all appearance settings.
        """

        self.apply_theme()

        self.apply_ui_scale()

        self.apply_status_bar()

        self.apply_bookmark_bar()

    # =================================================
    # Theme
    # =================================================

    def apply_theme(self) -> None:
        """
        Apply application theme.
        """

        theme = self.settings.theme

        if theme == "dark":

            self._apply_dark_theme()

        elif theme == "light":

            self._apply_light_theme()

        else:

            self._apply_system_theme()

    # -------------------------------------------------

    def set_theme(
        self,
        theme: str,
    ) -> None:

        self.settings.theme = theme

        self.apply_theme()

    # =================================================
    # UI Scale
    # =================================================

    def apply_ui_scale(self) -> None:
        """
        Apply UI scale setting.

        توجه:
        Qt در سطح Application به صورت مستقیم
        scale درصدی برای تمام Widgetها ارائه
        نمی‌کند.

        بنابراین فعلاً مقدار تنظیم ذخیره می‌شود
        و Zoom مرورگر جداگانه مدیریت خواهد شد.
        """

        value = self.settings.value(
            SettingsKeys.UI_SCALE,
            100,
        )

        try:

            value = int(value)

        except (
            TypeError,
            ValueError,
        ):

            value = 100

        value = max(
            50,
            min(
                value,
                200,
            ),
        )

        # فعلاً فقط مقدار معتبر نگه داشته می‌شود.
        #
        # اعمال واقعی Scale را بعداً در یک
        # UI Scale Manager انجام می‌دهیم.

    # =================================================
    # Status Bar
    # =================================================

    def apply_status_bar(self) -> None:
        """
        Apply status bar visibility.

        MainWindow در زمان اجرای این متد
        باید در دسترس باشد.

        فعلاً مقدار تنظیم فقط اعتبارسنجی می‌شود.
        """

        value = self.settings.value(
            SettingsKeys.SHOW_STATUS_BAR,
            True,
        )

        return bool(value)

    # =================================================
    # Bookmark Bar
    # =================================================

    def apply_bookmark_bar(self) -> None:
        """
        Apply bookmark bar visibility.

        نمایش واقعی Bookmark Bar بعد از
        پیاده‌سازی Bookmark UI انجام می‌شود.
        """

        value = self.settings.value(
            SettingsKeys.SHOW_BOOKMARK_BAR,
            False,
        )

        return bool(value)

    # =================================================
    # Theme Implementations
    # =================================================

    def _apply_dark_theme(self) -> None:
        """
        Apply dark application palette.
        """

        palette = self.application.palette()

        palette.setColor(
            palette.Window,
            Qt.GlobalColor.darkGray,
        )

        palette.setColor(
            palette.WindowText,
            Qt.GlobalColor.white,
        )

        palette.setColor(
            palette.Base,
            Qt.GlobalColor.black,
        )

        palette.setColor(
            palette.AlternateBase,
            Qt.GlobalColor.darkGray,
        )

        palette.setColor(
            palette.Text,
            Qt.GlobalColor.white,
        )

        palette.setColor(
            palette.Button,
            Qt.GlobalColor.darkGray,
        )

        palette.setColor(
            palette.ButtonText,
            Qt.GlobalColor.white,
        )

        self.application.setPalette(
            palette
        )

    # -------------------------------------------------

    def _apply_light_theme(self) -> None:
        """
        Apply light application palette.
        """

        self.application.setPalette(
            self.application.style().standardPalette()
        )

    # -------------------------------------------------

    def _apply_system_theme(self) -> None:
        """
        Restore system/application default palette.
        """

        self.application.setPalette(
            self.application.style().standardPalette()
        )