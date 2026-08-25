import re
from core.router import route

PIPELINE_ACTION = "ACTION_TASK"
PIPELINE_QUESTION = "GENERAL_QUESTION"

def classify_intent(text):
    """
    Classify user query into:
    1. ACTION_TASK: Immediate system control / tool execution (<10ms instant response, 0 LLM latency)
    2. GENERAL_QUESTION: Knowledge query or conversation (routed to fast local LLM model)
    """
    action, payload = route(text)
    
    if action != "chat":
        return PIPELINE_ACTION, action, payload
    
    return PIPELINE_QUESTION, "chat", text

def process_query_pipeline(user_input):
    """
    Dual-Pipeline Query Handler:
    - Fast-track actions without LLM latency.
    - Route general knowledge questions to model conversation.
    """
    intent_type, action, payload = classify_intent(user_input)
    return intent_type, action, payload
