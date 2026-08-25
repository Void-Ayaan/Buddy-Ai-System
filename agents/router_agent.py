from core.pipeline import process_query_pipeline

class RouterAgent:
    """AGENT-01: Intent Classification & Dual-Pipeline Dispatcher."""
    def __init__(self):
        self.agent_id = "AGENT-01"
        self.name = "ROUTER-NODE"

    def process(self, user_input):
        return process_query_pipeline(user_input)
