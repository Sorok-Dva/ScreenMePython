
# ScreenMe

ScreenMe is a screenshot utility that allows you to capture screenshots, select specific areas, and edit them with tools like adding text, shapes (circle, rectangle, arrow), and changing colors. The application also provides options to configure hotkeys, image format, image quality, and the default save folder.

## ⚠️ Unmaintened 

The ScreenMe project was initially designed with Python, but it was preferable to use another language, like C++. As a result, the Python version of the project is now discontinued, but the C++ version has been finalized and is available here : [ScreenMe](https://github.com/Sorok-Dva/ScreenMe)

## Features

- Capture full screen or selected area screenshots.
- Edit screenshots by adding text, circles, rectangles, and arrows.
- Customize the color palette for added elements.
- Configure hotkeys for taking screenshots.
- Choose between JPG and PNG image formats.
- Set image quality.
- Configure the default save folder.
- Start with the system.

## Installation

### Prerequisites

- Python > 3.4 or < 3.9
- PyQt5
- PyAutoGUI
- PyStray
- Keyboard
- Pillow

### Steps

1. Clone the repository:

```bash
git clone https://github.com/Sorok-Dva/ScreenMe.git
cd ScreenMe
```

2. Create and activate a virtual environment:

```bash
python -m venv env
env\Scripts\activate  # On Windows
source env/bin/activate  # On Linux/MacOS
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python main.py
```

## Building the Executable

To build an executable for the application, follow these steps:

1. Make sure you have PyInstaller installed:

```bash
pip install pyinstaller
```

2. Run the build script:

```bash
python build_exe.py
```

This will generate a `ScreenMe.exe` file in the project directory.

## Usage

- **Take Screenshot**: Press the configured hotkey (default is `Print Screen`) to take a screenshot.
- **Options**: Right-click on the system tray icon and select "Options" to configure settings.
- **Exit**: Right-click on the system tray icon and select "Exit" to close the application.

## Configuration

The application settings can be configured through the options window, accessible from the system tray icon. The settings are saved in `resources/config.json`.

### Configuration Options

- **Screenshot Hotkey**: Set the hotkey for taking a screenshot.
- **Fullscreen Screenshot Hotkey**: Set the hotkey for taking a fullscreen screenshot.
- **File Extension**: Choose between PNG and JPG formats.
- **Image Quality**: Set the quality of the image (1-100).
- **Default Save Folder**: Set the default folder where screenshots will be saved.
- **Start with System**: Enable or disable starting the application with the system.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch with your feature or bug fix.
3. Commit your changes.
4. Push to the branch.
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro)
- [PyAutoGUI](https://pyautogui.readthedocs.io/)
- [PyStray](https://github.com/moses-palmer/pystray)
- [Keyboard](https://github.com/boppreh/keyboard)
- [Pillow](https://python-pillow.org/)
