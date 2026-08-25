import os
import datetime
from PIL import ImageGrab

SCREENSHOT_DIR = "screenshots"

def take_screenshot():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)

    try:
        image = ImageGrab.grab()
        image.save(filepath)
        os.startfile(filepath)
        return f"Screenshot captured and saved to {filepath}."
    except Exception as e:
        return f"Failed to capture screenshot: {e}"
