import pyscreenshot as ImageGrab
import os

def capture_screen(config):
    # Capture the entire screen
    im = ImageGrab.grab()
    save_path = os.path.join(config['default_save_folder'], f"screenshot.{config['file_extension']}")
    if config['file_extension'] == 'jpg':
        im = im.convert('RGB')
        im.save(save_path, quality=config['image_quality'])
    else:
        im.save(save_path, quality=config['image_quality'])
