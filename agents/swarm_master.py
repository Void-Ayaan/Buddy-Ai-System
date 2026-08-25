from agents.router_agent import RouterAgent
from agents.oracle_agent import OracleAgent
from agents.vision_agent import VisionAgent
from agents.system_agent import SystemAgent
from agents.network_agent import NetworkAgent
from agents.security_agent import SecurityAgent
from agents.storage_agent import StorageAgent
from agents.media_agent import MediaAgent
from agents.search_agent import SearchAgent
from agents.workflow_agent import WorkflowAgent
from agents.learner_agent import LearnerAgent

class SwarmMaster:
    """Master Orchestrator managing real-time AI Agent Swarm topology across 11 sub-agents."""
    def __init__(self):
        self.router = RouterAgent()
        self.oracle = OracleAgent()
        self.vision = VisionAgent()
        self.system = SystemAgent()
        self.network = NetworkAgent()
        self.security = SecurityAgent()
        self.storage = StorageAgent()
        self.media = MediaAgent()
        self.search = SearchAgent()
        self.workflow = WorkflowAgent()
        self.learner = LearnerAgent()
        self.active_agent = "AGENT-01"
        self.last_target = "ROUTER-NODE"

    def set_active_workflow(self, action):
        """Map every user intent action to its corresponding active sub-agent node."""
        if action in ["learn_topic", "make_master_prompt", "word_definition", "get_capabilities"]:
            self.active_agent = "AGENT-11"
            self.last_target = "KNOWLEDGE-LEARNER"
        elif action in ["capture_vision"]:
            self.active_agent = "AGENT-03"
            self.last_target = "VISION-OPTIK"
        elif action in ["chat", "get_mood", "remember", "recall", "get_joke", "get_fact", "get_quote"]:
            self.active_agent = "AGENT-02"
            self.last_target = "KNOWLEDGE-ORACLE"
        elif action in ["check_ping", "check_wifi", "speed_test", "network_info", "check_website"]:
            self.active_agent = "AGENT-05"
            self.last_target = "NETWORK-PILOT"
        elif action in ["kill_process", "generate_password", "lock_pc", "sleep_pc", "shutdown_pc", "restart_pc", "cancel_shutdown"]:
            self.active_agent = "AGENT-06"
            self.last_target = "SECURITY-SHIELD"
        elif action in ["empty_recycle_bin", "disk_storage", "clean_temp", "organize_files", "move_file", "copy_file", "delete_file", "find_file", "save_code_desktop", "locate_code_file"]:
            self.active_agent = "AGENT-07"
            self.last_target = "STORAGE-MASTER"
        elif action in ["volume_up", "volume_down", "toggle_mute", "play_pause", "next_track", "previous_track", "sound_test", "set_volume_percent", "fix_mic", "dictation"]:
            self.active_agent = "AGENT-08"
            self.last_target = "MEDIA-PILOT"
        elif action in ["google_search", "youtube_search", "wiki_search", "get_news", "weather"]:
            self.active_agent = "AGENT-09"
            self.last_target = "WEB-SEARCH"
        elif action in ["coding_mode", "work_mode", "relax_mode", "self_upgrade", "add_note", "get_notes", "clear_notes", "timer"]:
            self.active_agent = "AGENT-10"
            self.last_target = "WORKFLOW-EXEC"
        elif action in ["jarvis_scan", "system_info", "optimize_ram", "battery_details", "health_check", "get_uptime", "top_processes", "calculate_math", "convert_units", "time", "date", "open_chrome", "open_url", "open_app", "close_app", "minimize", "screenshot", "read_clipboard", "copy_clipboard"]:
            self.active_agent = "AGENT-04"
            self.last_target = "SYSTEM-EXEC"
        else:
            self.active_agent = "AGENT-01"
            self.last_target = "ROUTER-NODE"

    def get_real_swarm_telemetry(self):
        """Return real-time statuses for all 11 sub-agents."""
        agents = [
            {"id": "AGENT-01", "name": "ROUTER", "status": "WORKING" if self.active_agent == "AGENT-01" else "IDLE"},
            {"id": "AGENT-02", "name": "ORACLE", "status": "WORKING" if self.active_agent == "AGENT-02" else "IDLE"},
            {"id": "AGENT-03", "name": "VISION", "status": "WORKING" if self.active_agent == "AGENT-03" else "IDLE"},
            {"id": "AGENT-04", "name": "SYSTEM", "status": "WORKING" if self.active_agent == "AGENT-04" else "IDLE"},
            {"id": "AGENT-05", "name": "NETWORK", "status": "WORKING" if self.active_agent == "AGENT-05" else "IDLE"},
            {"id": "AGENT-06", "name": "SECURITY", "status": "WORKING" if self.active_agent == "AGENT-06" else "IDLE"},
            {"id": "AGENT-07", "name": "STORAGE", "status": "WORKING" if self.active_agent == "AGENT-07" else "IDLE"},
            {"id": "AGENT-08", "name": "MEDIA", "status": "WORKING" if self.active_agent == "AGENT-08" else "IDLE"},
            {"id": "AGENT-09", "name": "SEARCH", "status": "WORKING" if self.active_agent == "AGENT-09" else "IDLE"},
            {"id": "AGENT-10", "name": "WORKFLOW", "status": "WORKING" if self.active_agent == "AGENT-10" else "IDLE"},
            {"id": "AGENT-11", "name": "LEARNER", "status": "WORKING" if self.active_agent == "AGENT-11" else "IDLE"},
        ]
        return {
            "agents": agents,
            "connection": {
                "from": "ROUTER-NODE",
                "to": self.last_target
            }
        }

swarm = SwarmMaster()
