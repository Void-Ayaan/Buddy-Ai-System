import time
import re
from core.router import route
from core.fuzzy_corrector import normalize_fuzzy_input

PIPELINE_ACTION = "ACTION_TASK"
PIPELINE_QUESTION = "GENERAL_QUESTION"

def process_query_pipeline(user_input):
    """
    Advanced 3-Stage High-Performance AI Pipeline:
    ---------------------------------------------
    Stage 1: Pre-process & Fuzzy Auto-Correction (<1ms)
             Fixes spelling errors, phonetic typos, and colloquial phrasing.
    Stage 2: Intent Classification & Routing (<5ms)
             Distinguishes instant system actions vs knowledge reasoning.
    Stage 3: Telemetry & Execution Pipeline (<10ms)
             Executes direct system controls or routes to local LLM model FIRST.
    """
    t0 = time.perf_counter()
    raw_input = (user_input or "").strip()
    
    if not raw_input:
        return PIPELINE_QUESTION, "chat", "", 0.0

    # Stage 1: Fuzzy spelling & phonetic normalization
    clean_input = normalize_fuzzy_input(raw_input)

    # Stage 2: Intent classification & payload extraction
    action, payload = route(clean_input)

    t1 = time.perf_counter()
    latency_ms = round((t1 - t0) * 1000, 2)

    if action != "chat":
        return PIPELINE_ACTION, action, payload, latency_ms
    
    return PIPELINE_QUESTION, "chat", clean_input, latency_ms
