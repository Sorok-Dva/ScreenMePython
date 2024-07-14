import json

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.default_config = {
            "screenshot_hotkey": "Ctrl+Shift+S",
            "fullscreen_hotkey": "Ctrl+Shift+F",
            "file_extension": "png",
            "default_save_folder": ".",
            "start_with_system": False,
            "image_quality": 90
        }
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.config_path, 'r') as file:
                config = json.load(file)
        except FileNotFoundError:
            config = self.default_config
            self.save_config(config)
        return config

    def save_config(self, config):
        with open(self.config_path, 'w') as file:
            json.dump(config, file, indent=4)

    def get_config(self):
        return self.config

    def update_config(self, key, value):
        self.config[key] = value
        self.save_config(self.config)
