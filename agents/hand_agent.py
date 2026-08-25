from tools.hand_gesture_tools import toggle_hand_controller, get_hand_telemetry

class HandAgent:
    """AGENT-12: Hand Gesture Controller, Pinch Kinematics, and 3D Swarm Scaling."""
    def __init__(self):
        self.agent_id = "AGENT-12"
        self.name = "HAND-KINEMATIK"

    def activate(self, enable=True):
        return toggle_hand_controller(enable)

    def telemetry(self):
        return get_hand_telemetry()
