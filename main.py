import sys
import os
from PyQt5.QtWidgets import QApplication, QAction, QMenu, QSystemTrayIcon, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer, QMetaObject, Q_ARG, pyqtSlot
import keyboard
import pyautogui
from editor.editor import Editor
from editor.config_manager import ConfigManager
from settings.options import OptionsWindow

class MainApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.setQuitOnLastWindowClosed(False)  # Prevent application from quitting when last window is closed
        self.config_manager = ConfigManager("resources/config.json")
        self.tray_icon = QSystemTrayIcon(QIcon("resources/icon.png"))
        self.main_window = QMainWindow()  # Dummy window to anchor the tray icon
        self.init_tray_icon()
        self.tray_icon.show()
        self.load_hotkeys()

    def init_tray_icon(self):
        menu = QMenu()

        capture_action = QAction("Take Screenshot", self.main_window)
        capture_action.triggered.connect(lambda: QTimer.singleShot(0, self.take_screenshot))
        menu.addAction(capture_action)

        fullscreen_action = QAction("Take Fullscreen Screenshot", self.main_window)
        fullscreen_action.triggered.connect(lambda: QTimer.singleShot(0, self.take_fullscreen_screenshot))
        menu.addAction(fullscreen_action)

        options_action = QAction("Options", self.main_window)
        options_action.triggered.connect(self.show_options)
        menu.addAction(options_action)

        exit_action = QAction("Exit", self.main_window)
        exit_action.triggered.connect(self.exit_app)
        menu.addAction(exit_action)

        self.tray_icon.setContextMenu(menu)

    def load_hotkeys(self):
        config = self.config_manager.load_config()
        screenshot_key = config.get('screenshot_hotkey', 'print_screen')
        fullscreen_key = config.get('fullscreen_hotkey', 'f11')

        if screenshot_key:
            keyboard.add_hotkey(screenshot_key, lambda: QTimer.singleShot(0, self.take_screenshot))
        if fullscreen_key:
            keyboard.add_hotkey(fullscreen_key, lambda: QTimer.singleShot(0, self.take_fullscreen_screenshot))

    def take_screenshot(self):
        QTimer.singleShot(0, self._take_screenshot)

    def _take_screenshot(self):
        try:
            screenshot = pyautogui.screenshot()
            config = self.config_manager.load_config()
            save_path = self.get_unique_filepath(config['default_save_folder'], "screenshot", config['file_extension'])
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            screenshot.save(save_path)
            QMetaObject.invokeMethod(self, "create_editor", Qt.QueuedConnection)
        except Exception as e:
            QMetaObject.invokeMethod(self, "display_error_message", Qt.QueuedConnection, Q_ARG(str, "Screenshot Error"), Q_ARG(str, str(e)))

    def take_fullscreen_screenshot(self):
        QTimer.singleShot(0, self._take_fullscreen_screenshot)

    def _take_fullscreen_screenshot(self):
        try:
            screenshot = pyautogui.screenshot()
            config = self.config_manager.load_config()
            save_path = self.get_unique_filepath(config['default_save_folder'], "fullscreen_screenshot", config['file_extension'])
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            screenshot.save(save_path)
            QMetaObject.invokeMethod(self, "create_editor", Qt.QueuedConnection)
        except Exception as e:
            QMetaObject.invokeMethod(self, "display_error_message", Qt.QueuedConnection, Q_ARG(str, "Screenshot Error"), Q_ARG(str, str(e)))

    @pyqtSlot()
    def create_editor(self):
        editor = Editor(self.config_manager)
        editor.show()

    def get_unique_filepath(self, folder, base_name, extension):
        os.makedirs(folder, exist_ok=True)
        i = 1
        while True:
            filename = f"{base_name}-{i}.{extension}"
            filepath = os.path.join(folder, filename)
            if not os.path.exists(filepath):
                return filepath
            i += 1

    def show_options(self):
        options_window = OptionsWindow(self.config_manager)
        options_window.setAttribute(Qt.WA_QuitOnClose, False)  # Ensure this window does not close the app
        options_window.exec_()

    @pyqtSlot(str, str)
    def display_error_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def exit_app(self):
        keyboard.unhook_all_hotkeys()
        self.quit()

if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
