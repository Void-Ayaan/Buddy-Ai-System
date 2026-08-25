from tools.recycle_tools import empty_recycle_bin
from tools.disk_analyzer import analyze_disk_storage
from tools.cleanup_tools import clean_temp_files

class StorageAgent:
    """AGENT-07: Disk Storage Analysis, Recycle Bin Purge, and Temp Cleanup."""
    def __init__(self):
        self.agent_id = "AGENT-07"
        self.name = "STORAGE-MASTER"

    def empty_bin(self):
        return empty_recycle_bin()

    def analyze_storage(self):
        return analyze_disk_storage()

    def clean_temp(self):
        return clean_temp_files()
