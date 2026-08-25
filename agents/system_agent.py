from tools.ram_cleaner import optimize_ram_memory
from tools.cleanup_tools import clean_temp_files
from tools.jarvis_hud import run_buddy_system_scan
from tools.power_tools import lock_pc, sleep_pc, shutdown_pc, restart_pc, cancel_shutdown
from tools.volume_slider import parse_volume_command
from tools.system_tools import open_app, close_app, minimize_window, get_system_info

class SystemAgent:
    """AGENT-04: Windows OS Execution, Power Controls, and Hardware HUD."""
    def __init__(self):
        self.agent_id = "AGENT-04"
        self.name = "SYSTEM-EXEC"

    def optimize_ram(self):
        return optimize_ram_memory()

    def clean_temp(self):
        return clean_temp_files()

    def scan_hud(self):
        return run_buddy_system_scan()

    def lock(self):
        return lock_pc()

    def sys_info(self):
        return get_system_info()
