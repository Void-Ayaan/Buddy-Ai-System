from tools.camera_tools import capture_vision
from tools.screen_tools import take_screenshot

class VisionAgent:
    """AGENT-03: Camera Vision, Facial Detection, and Screen Diagnostics."""
    def __init__(self):
        self.agent_id = "AGENT-03"
        self.name = "VISION-OPTIK"

    def see(self):
        return capture_vision()

    def snap_screen(self):
        return take_screenshot()
