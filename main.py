import sys
from PyQt5.QtWidgets import QApplication, QAction, QMenu, QSystemTrayIcon, QMessageBox, QMainWindow
from PyQt5.QtGui import QIcon
import keyboard
import pyautogui
import os
from editor.editor import Editor
from editor.config_manager import ConfigManager
from settings.options import OptionsWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager("resources/config.json")
        self.initUI()

    def initUI(self):
        self.tray_icon = QSystemTrayIcon(QIcon("resources/icon.png"), self)
        self.create_tray_icon()
        self.tray_icon.show()
        self.hide()

        self.load_hotkeys()

    def load_hotkeys(self):
        config = self.config_manager.load_config()
        screenshot_key = config.get('screenshot_hotkey', 'print_screen')
        fullscreen_key = config.get('fullscreen_hotkey', 'f11')

        if screenshot_key:
            keyboard.add_hotkey(screenshot_key, self.take_screenshot)
        if fullscreen_key:
            keyboard.add_hotkey(fullscreen_key, self.take_fullscreen_screenshot)

    def take_screenshot(self):
        screenshot = pyautogui.screenshot()
        config = self.config_manager.load_config()
        save_path = os.path.join(config['default_save_folder'], f"screenshot.{config['file_extension']}")
        screenshot.save(save_path)
        editor = Editor(self.config_manager)
        editor.show()

    def take_fullscreen_screenshot(self):
        screenshot = pyautogui.screenshot()
        config = self.config_manager.load_config()
        save_path = os.path.join(config['default_save_folder'], f"fullscreen_screenshot.{config['file_extension']}")
        screenshot.save(save_path)
        editor = Editor(self.config_manager)
        editor.show()

    def create_tray_icon(self):
        menu = QMenu()

        capture_action = QAction("Take Screenshot", self)
        capture_action.triggered.connect(self.take_screenshot)
        menu.addAction(capture_action)

        options_action = QAction("Options", self)
        options_action.triggered.connect(self.show_options)
        menu.addAction(options_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_app)
        menu.addAction(exit_action)

        self.tray_icon.setContextMenu(menu)

    def show_options(self):
        options_window = OptionsWindow(self.config_manager)
        options_window.exec_()

    def exit_app(self):
        keyboard.unhook_all_hotkeys()
        QApplication.instance().quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
