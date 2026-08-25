from tools.password_tools import generate_secure_password
from tools.kill_tools import kill_named_process

class SecurityAgent:
    """AGENT-06: Security Protocol, Process Termination, and Cryptographic Shield."""
    def __init__(self):
        self.agent_id = "AGENT-06"
        self.name = "SECURITY-SHIELD"

    def generate_pass(self):
        return generate_secure_password()

    def kill_proc(self, process_name):
        return kill_named_process(process_name)
