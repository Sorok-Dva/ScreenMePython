from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox, QSpinBox, QCheckBox
from PyQt5.QtCore import Qt
import keyboard

class OptionsWindow(QDialog):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.config = self.config_manager.load_config()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Options')
        layout = QVBoxLayout()

        # Screenshot hotkey
        layout.addWidget(QLabel('Screenshot Hotkey:'))
        self.hotkey_edit = QLineEdit(self.config['screenshot_hotkey'])
        self.hotkey_edit.setPlaceholderText('Press any key...')
        self.hotkey_edit.setReadOnly(True)
        self.hotkey_edit.mousePressEvent = self.record_hotkey
        layout.addWidget(self.hotkey_edit)

        # Fullscreen hotkey
        layout.addWidget(QLabel('Fullscreen Screenshot Hotkey:'))
        self.fullscreen_hotkey_edit = QLineEdit(self.config['fullscreen_hotkey'])
        self.fullscreen_hotkey_edit.setPlaceholderText('Press any key...')
        self.fullscreen_hotkey_edit.setReadOnly(True)
        self.fullscreen_hotkey_edit.mousePressEvent = self.record_fullscreen_hotkey
        layout.addWidget(self.fullscreen_hotkey_edit)

        # File extension
        layout.addWidget(QLabel('File Extension:'))
        self.extension_combo = QComboBox()
        self.extension_combo.addItems(['png', 'jpg'])
        self.extension_combo.setCurrentText(self.config['file_extension'])
        layout.addWidget(self.extension_combo)

        # Image quality
        layout.addWidget(QLabel('Image Quality:'))
        self.quality_spinbox = QSpinBox()
        self.quality_spinbox.setRange(1, 100)
        self.quality_spinbox.setValue(self.config['image_quality'])
        layout.addWidget(self.quality_spinbox)

        # Default save folder
        layout.addWidget(QLabel('Default Save Folder:'))
        self.folder_edit = QLineEdit(self.config['default_save_folder'])
        self.folder_button = QPushButton('Browse')
        self.folder_button.clicked.connect(self.select_folder)
        layout.addWidget(self.folder_edit)
        layout.addWidget(self.folder_button)

        # Start with system
        self.start_with_system_checkbox = QCheckBox('Start with system')
        self.start_with_system_checkbox.setChecked(self.config['start_with_system'])
        layout.addWidget(self.start_with_system_checkbox)

        # Save button
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_options)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def record_hotkey(self, event):
        self.hotkey_edit.setText('')
        self.hotkey_edit.setPlaceholderText('Press any key...')
        keyboard.start_recording()
        keys = keyboard.get_hotkey_name(keyboard.stop_recording())
        self.hotkey_edit.setText(keys)

    def record_fullscreen_hotkey(self, event):
        self.fullscreen_hotkey_edit.setText('')
        self.fullscreen_hotkey_edit.setPlaceholderText('Press any key...')
        keyboard.start_recording()
        keys = keyboard.get_hotkey_name(keyboard.stop_recording())
        self.fullscreen_hotkey_edit.setText(keys)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            self.folder_edit.setText(folder)

    def save_options(self):
        self.config['screenshot_hotkey'] = self.hotkey_edit.text()
        self.config['fullscreen_hotkey'] = self.fullscreen_hotkey_edit.text()
        self.config['file_extension'] = self.extension_combo.currentText()
        self.config['image_quality'] = self.quality_spinbox.value()
        self.config['default_save_folder'] = self.folder_edit.text()
        self.config['start_with_system'] = self.start_with_system_checkbox.isChecked()

        self.config_manager.save_config(self.config)
        self.accept()  # Ferme la fenêtre après avoir enregistré les options
