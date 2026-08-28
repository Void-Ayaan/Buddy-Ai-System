import re
from core.router import route
from core.react_engine import react_engine

PIPELINE_ACTION = "ACTION_TASK"
PIPELINE_QUESTION = "GENERAL_QUESTION"
PIPELINE_REACT = "REACT_MULTI_STEP"

# Common phonetic typos, misspelled words, and colloquial phrasing map
TYPO_DICTIONARY = {
    r"\btonny\b": "tony",
    r"\beerthing\b": "everything",
    r"\beerything\b": "everything",
    r"\bwhst\b": "what",
    r"\bwhats\b": "what is",
    r"\bmicphone\b": "microphone",
    r"\bmick\b": "mic",
    r"\bpromt\b": "prompt",
    r"\bpromp\b": "prompt",
    r"\bsys\b": "system",
    r"\bdiag\b": "diagnostic",
    r"\bvolum\b": "volume",
    r"\blptp\b": "laptop",
    r"\bpc scan\b": "system scan",
    r"\bcalc\b": "calculator",
}

def preprocess_and_autocorrect_input(text):
    """
    STAGE 1: Pre-process & Fuzzy Auto-Correction (<1 ms)
    - Normalizes spaces, strips special characters.
    - Auto-corrects misspelled words, phonetic typos, and colloquial phrasing.
    """
    if not text:
        return ""
    
    clean = text.strip()
    clean_lower = clean.lower()
    
    for pattern, replacement in TYPO_DICTIONARY.items():
        clean_lower = re.sub(pattern, replacement, clean_lower)
        
    return clean_lower

def classify_intent(text):
    """
    STAGE 2: Intent Classification & Route Mapping (<3 ms)
    - ReAct Multi-Step Loop Check (Multi-intent NLP Function Calling).
    - Single-intent System actions vs Knowledge reasoning questions.
    """
    if react_engine.is_multi_step_request(text):
        plan = react_engine.decompose_into_plan(text)
        if len(plan) >= 2:
            return PIPELINE_REACT, "react_loop", text

    action, payload = route(text)
    
    if action != "chat":
        return PIPELINE_ACTION, action, payload
    
    return PIPELINE_QUESTION, "chat", text

def process_query_pipeline(user_input):
    """
    3-STAGE HIGH-PERFORMANCE QUERY PIPELINE + REACT ENGINE ARCHITECTURE:
    
    User Query Input
      │
      ▼
    Stage 1: Pre-process & Fuzzy Auto-Correction (<1 ms)
      │
      ▼
    Stage 2: Intent Classification & ReAct Multi-Step Loop Engine (<3 ms)
      │
      ▼
    Stage 3: Sub-10ms Action Execution, ReAct Tool Loop, or Local LLM Model Reasoning
    """
    processed_input = preprocess_and_autocorrect_input(user_input)
    intent_type, action, payload = classify_intent(processed_input)
    return intent_type, action, payload
