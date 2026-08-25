import ctypes
import re

def set_volume_percentage(percent):
    """Set system master volume roughly to requested percentage (0 - 100)."""
    try:
        percent = max(0, min(100, int(percent)))
        
        # Approximate step using volume down to 0 then volume up
        VK_VOLUME_MUTE = 0xAD
        VK_VOLUME_DOWN = 0xAE
        VK_VOLUME_UP = 0xAF

        # First, send 50 volume down key presses to zero out volume
        for _ in range(50):
            ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, 2, 0)

        # Each volume up keypress increments by 2%
        up_clicks = int(percent / 2)
        for _ in range(up_clicks):
            ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 2, 0)

        return f"Set system volume to approximately {percent} percent, Boss!"
    except Exception as e:
        return f"Could not set volume: {e}"

def parse_volume_command(text):
    text_lower = text.lower().strip()
    match = re.search(r"(\d+)\s*%?", text_lower)
    if match:
        vol = int(match.group(1))
        return set_volume_percentage(vol)
    
    if "max" in text_lower or "full" in text_lower:
        return set_volume_percentage(100)
    if "half" in text_lower:
        return set_volume_percentage(50)
        
    return "Please specify a volume percentage, like 'set volume to 50 percent'."
