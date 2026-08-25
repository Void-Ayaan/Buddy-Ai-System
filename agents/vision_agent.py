from tools.camera_tools import capture_vision, toggle_live_vision
from tools.screen_tools import take_screenshot

class VisionAgent:
    """AGENT-03: Camera Vision, Facial Detection, Motion Monitoring, and Screen Diagnostics."""
    def __init__(self):
        self.agent_id = "AGENT-03"
        self.name = "VISION-OPTIK"

    def see(self):
        return capture_vision()

    def live_eye(self, enable=True):
        return toggle_live_vision(enable)

    def snap_screen(self):
        return take_screenshot()
