from core.llm import ask_ai
from memory.cache_manager import get_cached_response, save_cached_response

class OracleAgent:
    """AGENT-02: LLM Knowledge Reasoning & Cache Manager."""
    def __init__(self):
        self.agent_id = "AGENT-02"
        self.name = "KNOWLEDGE-ORACLE"

    def answer_question(self, question):
        cached = get_cached_response(question)
        if cached:
            return cached, True # Hit cache
        
        ans = ask_ai(question)
        save_cached_response(question, ans)
        return ans, False
