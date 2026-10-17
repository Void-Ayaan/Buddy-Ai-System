import os
import sys
import json
import time
from datetime import datetime
import re
import logging
import threading
import difflib
import random

logger = logging.getLogger("buddy.proactive")

# Configuration Constants
DEFAULT_ENABLED = False
TICK_SECONDS = 900          # 15 minutes
MIN_GAP_SECONDS = 2700      # 45 minutes
DAILY_MAX = 8               # Max proactive utterances per day
QUIET_HOURS_START = 23      # 23:00 (11 PM)
QUIET_HOURS_END = 7         # 07:00 (7 AM)
USER_IDLE_SECONDS = 300     # 5 minutes idle time required
MAX_RESPONSE_CHARS = 300
MAX_RESPONSE_TOKENS = 120
TEMPERATURE = 0.8

TOPIC_CATEGORIES = [
    "science", "history", "geography", "animals", "food",
    "music", "sports", "technology", "language", "weather",
    "space", "art", "everyday life", "ocean", "invention"
]

COMMON_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can",
    "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't",
    "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
    "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him",
    "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't",
    "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor",
    "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out",
    "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some",
    "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there",
    "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to",
    "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's",
    "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're",
    "you've", "your", "yours", "yourself", "yourselves"
}

def extract_content_words(text):
    """Extract lowercase words with stopwords removed."""
    if not text:
        return set()
    tokens = re.findall(r"\b[a-zA-Z]{2,}\b", text.lower())
    return {w for w in tokens if w not in COMMON_STOPWORDS}

def extract_content_word_list(text):
    """Extract lowercase words with stopwords removed, preserving sequential order."""
    if not text:
        return []
    tokens = re.findall(r"\b[a-zA-Z]{2,}\b", text.lower())
    return [w for w in tokens if w not in COMMON_STOPWORDS]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_DIR = os.path.join(BASE_DIR, "memory")
STATE_FILE = os.path.join(MEMORY_DIR, "proactive_state.json")
LOG_FILE = os.path.join(MEMORY_DIR, "proactive_log.json")
LOCK_FILE = os.path.join(MEMORY_DIR, "proactive_scheduler.lock")
SECRET_FILE = os.path.join(MEMORY_DIR, "proactive_secret.txt")

# State and log concurrency synchronization locks
STATE_LOCK = threading.RLock()
LOG_LOCK = threading.RLock()

def get_or_create_proactive_secret():
    """
    Load or generate a cryptographically secure shared secret for proactive HTTP IPC.
    Persisted to memory/proactive_secret.txt.
    """
    if os.path.exists(SECRET_FILE):
        try:
            with open(SECRET_FILE, "r", encoding="utf-8") as f:
                secret = f.read().strip()
                if secret:
                    return secret
        except Exception as e:
            logger.warning(f"[Proactive] Failed reading secret file {SECRET_FILE}: {e}")

    import secrets
    new_secret = secrets.token_hex(32)
    try:
        os.makedirs(MEMORY_DIR, exist_ok=True)
        with open(SECRET_FILE, "w", encoding="utf-8") as f:
            f.write(new_secret)
    except Exception as e:
        logger.error(f"[Proactive] Failed saving secret to {SECRET_FILE}: {e}")
    return new_secret

# Model concurrency synchronization and priority lock
MODEL_LOCK = threading.Lock()
_USER_INTERRUPT_FLAG = threading.Event()
_PROACTIVE_GENERATING = threading.Event()

# Active in-flight HTTP response handle for proactive calls
_ACTIVE_PROACTIVE_HTTP_RESP = None
_ACTIVE_PROACTIVE_HTTP_LOCK = threading.Lock()

def abort_active_proactive_call():
    """Immediately close in-flight HTTP request/stream and stop reading."""
    global _ACTIVE_PROACTIVE_HTTP_RESP
    with _ACTIVE_PROACTIVE_HTTP_LOCK:
        if _ACTIVE_PROACTIVE_HTTP_RESP is not None:
            try:
                _ACTIVE_PROACTIVE_HTTP_RESP.close()
            except Exception:
                pass
            _ACTIVE_PROACTIVE_HTTP_RESP = None

# User request pending tracker
_USER_WAITING_COUNT = 0
_USER_WAITING_LOCK = threading.Lock()

def mark_user_request_waiting(waiting: bool):
    """Track whether a user request is waiting on the model lock."""
    global _USER_WAITING_COUNT
    with _USER_WAITING_LOCK:
        if waiting:
            _USER_WAITING_COUNT += 1
        else:
            _USER_WAITING_COUNT = max(0, _USER_WAITING_COUNT - 1)

def is_user_request_waiting():
    """Check if any user query is currently waiting on the model lock."""
    with _USER_WAITING_LOCK:
        return _USER_WAITING_COUNT > 0

# Optional HUD notification callback and port tracking
_HUD_BROADCASTER = None
_HUD_BOUND_PORT = None

def set_hud_port(port: int):
    """Set the port that the HUD is bound to."""
    global _HUD_BOUND_PORT
    if isinstance(port, int) and port > 0:
        _HUD_BOUND_PORT = port

def get_hud_port() -> int:
    """Return the active port of the HUD, checking shared variable, port file, or fallback."""
    global _HUD_BOUND_PORT
    if _HUD_BOUND_PORT is not None:
        return _HUD_BOUND_PORT
    try:
        import ui.server
        p = getattr(ui.server, "ACTUAL_BOUND_PORT", None)
        if isinstance(p, int) and p > 0:
            return p
    except Exception:
        pass
    port_file = os.path.join(MEMORY_DIR, "hud_port.txt")
    if os.path.exists(port_file):
        try:
            with open(port_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content.isdigit():
                    return int(content)
        except Exception:
            pass
    return 5000

def register_hud_broadcaster(broadcaster_func):
    """Register a callback function to send messages to the HUD interface."""
    global _HUD_BROADCASTER
    _HUD_BROADCASTER = broadcaster_func

def load_proactive_state():
    """
    Read proactive state from memory/proactive_state.json.
    If the file is missing or invalid, treat as disabled by default.
    """
    default_state = {
        "enabled": DEFAULT_ENABLED,
        "last_user_activity": 0.0,
        "last_utterance": 0.0,
        "daily_count": 0,
        "daily_count_date": ""
    }
    with STATE_LOCK:
        if not os.path.exists(STATE_FILE):
            return default_state

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    return default_state
                # Ensure all expected keys have sensible fallbacks
                for k, v in default_state.items():
                    if k not in data:
                        data[k] = v
                return data
        except Exception as e:
            logger.warning(f"[Proactive] Could not read {STATE_FILE}: {e}")
            return default_state

def save_proactive_state(state):
    """Atomically write state dict to memory/proactive_state.json."""
    with STATE_LOCK:
        try:
            os.makedirs(MEMORY_DIR, exist_ok=True)
            temp_file = f"{STATE_FILE}.{threading.get_ident()}.tmp"
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
            for attempt in range(5):
                try:
                    os.replace(temp_file, STATE_FILE)
                    return True
                except PermissionError:
                    time.sleep(0.02)
            os.replace(temp_file, STATE_FILE)
            return True
        except Exception as e:
            logger.error(f"[Proactive] Failed to save state to {STATE_FILE}: {e}")
            return False

def touch_user_activity(timestamp=None):
    """Update last user activity timestamp in state."""
    with STATE_LOCK:
        state = load_proactive_state()
        ts = time.time() if timestamp is None else float(timestamp)
        state["last_user_activity"] = ts
        save_proactive_state(state)
        logger.debug(f"[Proactive] User activity recorded at {ts}")

def set_proactive_enabled(enabled: bool):
    """Enable or disable proactive speaking mode."""
    with STATE_LOCK:
        state = load_proactive_state()
        state["enabled"] = bool(enabled)
        save_proactive_state(state)
        logger.info(f"[Proactive] Mode enabled set to {state['enabled']}")
        return state["enabled"]

def is_quiet_hours(dt=None):
    """
    Check if the given local time falls within quiet hours (23:00 - 07:00).
    """
    now = dt if dt is not None else datetime.now()
    hour = now.hour
    return hour >= QUIET_HOURS_START or hour < QUIET_HOURS_END

def load_proactive_log_entries():
    """Load all logged entries from memory/proactive_log.json."""
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception as e:
        logger.warning(f"[Proactive] Failed reading log file {LOG_FILE}: {e}")
        return []

def get_recent_log_lines(count=30):
    """Return the text of the last N entries from proactive_log.json."""
    entries = load_proactive_log_entries()
    recent = entries[-count:] if len(entries) >= count else entries
    lines = []
    for item in recent:
        if isinstance(item, dict):
            text = item.get("text", "")
            if text:
                lines.append(text)
        elif isinstance(item, str):
            lines.append(item)
    return lines

def append_to_proactive_log(text, timestamp=None):
    """Append a spoken line to memory/proactive_log.json with an ISO timestamp."""
    with LOG_LOCK:
        entries = load_proactive_log_entries()
        ts_str = timestamp if timestamp is not None else datetime.now().isoformat()
        new_entry = {
            "timestamp": ts_str,
            "text": text
        }
        entries.append(new_entry)
        try:
            os.makedirs(MEMORY_DIR, exist_ok=True)
            temp_file = f"{LOG_FILE}.{threading.get_ident()}.{time.time_ns()}.tmp"
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(entries, f, indent=2)
            for attempt in range(5):
                try:
                    os.replace(temp_file, LOG_FILE)
                    return new_entry
                except PermissionError:
                    time.sleep(0.02)
            os.replace(temp_file, LOG_FILE)
            return new_entry
        except Exception as e:
            logger.error(f"[Proactive] Failed writing to log file {LOG_FILE}: {e}")
            return new_entry

def evaluate_tick_condition(now=None, state=None):
    """
    Check gating conditions in strict specification order:
    1. enabled
    2. quiet hours
    3. user active in last user_idle_seconds
    4. min_gap since last utterance
    5. daily_max not reached
    Returns the reason it skipped, or 'ready'.
    """
    current_dt = now if isinstance(now, datetime) else (datetime.fromtimestamp(now) if now is not None else datetime.now())
    current_ts = current_dt.timestamp()
    current_date_str = current_dt.strftime("%Y-%m-%d")

    current_state = state if state is not None else load_proactive_state()

    # 1. enabled
    if not current_state.get("enabled", False):
        return "disabled"

    # 2. quiet hours (23:00 - 07:00 local time)
    if is_quiet_hours(current_dt):
        return "quiet_hours"

    # 3. user active in last user_idle_seconds (300s)
    last_user_act = current_state.get("last_user_activity", 0.0)
    if last_user_act > 0 and (current_ts - last_user_act) < USER_IDLE_SECONDS:
        return "recently_active"

    # 4. min_gap since last utterance (2700s)
    last_utterance = current_state.get("last_utterance", 0.0)
    if last_utterance > 0 and (current_ts - last_utterance) < MIN_GAP_SECONDS:
        return "within_gap"

    # 5. daily_max not reached (8 utterances per day)
    state_date = current_state.get("daily_count_date", "")
    daily_count = current_state.get("daily_count", 0)
    if state_date == current_date_str and daily_count >= DAILY_MAX:
        return "daily_max_reached"

    return "ready"

def check_candidate_repetition(candidate_text, history_lines=None):
    """
    Check candidate proactive thought against recent history using 3 distinct rules:
    Rule 1: difflib SequenceMatcher ratio >= 0.6
    Rule 2: Content-word overlap >= 0.5 (stopwords removed)
    Rule 3: Shared 4-word sequence after stopword removal (4-gram match)

    Returns a dict with:
      - is_valid (bool)
      - rejection_reason (str or None)
      - nearest_line (str or None)
      - nearest_ratio (float)
      - nearest_overlap (float)
      - matched_4gram (tuple or None)
    """
    if history_lines is None:
        history_lines = get_recent_log_lines(30)

    cand_lower = candidate_text.lower().strip() if candidate_text else ""
    cand_content_words = extract_content_words(candidate_text)
    cand_word_list = extract_content_word_list(candidate_text)
    cand_4grams = {
        tuple(cand_word_list[i:i+4])
        for i in range(len(cand_word_list) - 3)
    } if len(cand_word_list) >= 4 else set()

    nearest_line = None
    nearest_ratio = 0.0
    nearest_overlap = 0.0
    rejection_reason = None
    is_valid = True
    matched_4gram = None

    for prev in history_lines:
        prev_lower = prev.lower().strip() if prev else ""
        ratio = difflib.SequenceMatcher(None, cand_lower, prev_lower).ratio()

        prev_content_words = extract_content_words(prev)
        overlap = (len(cand_content_words & prev_content_words) / len(cand_content_words)) if cand_content_words else 0.0

        prev_word_list = extract_content_word_list(prev)
        prev_4grams = {
            tuple(prev_word_list[i:i+4])
            for i in range(len(prev_word_list) - 3)
        } if len(prev_word_list) >= 4 else set()
        shared_4grams = cand_4grams & prev_4grams

        # Track nearest line by highest sequence similarity, then overlap
        if nearest_line is None or ratio > nearest_ratio:
            nearest_line = prev
            nearest_ratio = ratio
            nearest_overlap = overlap
        elif abs(ratio - nearest_ratio) < 0.001 and overlap > nearest_overlap:
            nearest_line = prev
            nearest_ratio = ratio
            nearest_overlap = overlap

        # Evaluation of Rule 1
        if ratio >= 0.6 and is_valid:
            is_valid = False
            rejection_reason = f"repetition_ratio_ge_0.6 (ratio={ratio:.2f})"

        # Evaluation of Rule 2
        if overlap >= 0.5 and is_valid:
            is_valid = False
            rejection_reason = f"content_word_overlap_ge_0.5 (overlap={overlap:.2f})"

        # Evaluation of Rule 3
        if shared_4grams and is_valid:
            is_valid = False
            matched_4gram = next(iter(shared_4grams))
            rejection_reason = f"shared_phrase_4gram ('{' '.join(matched_4gram)}')"

    return {
        "is_valid": is_valid,
        "rejection_reason": rejection_reason,
        "nearest_line": nearest_line,
        "nearest_ratio": round(nearest_ratio, 3),
        "nearest_overlap": round(nearest_overlap, 3),
        "matched_4gram": matched_4gram
    }

def query_proactive_model_stream(messages, max_tokens=120, temperature=0.8, timeout=30):
    """
    Direct OpenAI-compatible streaming query that monitors for user interruptions
    and can be aborted immediately from another thread by closing the HTTP response.
    Never accepts or uses any tool parameters.
    """
    global _ACTIVE_PROACTIVE_HTTP_RESP
    import urllib.request
    from core.llamafile_manager import LLAMAFILE_PORT
    url = f"http://127.0.0.1:{LLAMAFILE_PORT}/v1/chat/completions"
    payload = {
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True,
        "chat_template_kwargs": {"enable_thinking": False}
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
    except Exception as e:
        return None, f"connection_error: {e}"

    with _ACTIVE_PROACTIVE_HTTP_LOCK:
        _ACTIVE_PROACTIVE_HTTP_RESP = resp

    accumulated = []
    try:
        for raw_line in resp:
            # Abort check: if user request arrived, close stream and stop reading immediately
            if _USER_INTERRUPT_FLAG.is_set() or is_user_request_waiting():
                try:
                    resp.close()
                except Exception:
                    pass
                return None, "interrupted_by_user"

            line_str = raw_line.decode("utf-8", errors="replace").strip()
            if not line_str.startswith("data:"):
                continue
            data_str = line_str[5:].strip()
            if data_str == "[DONE]":
                break
            try:
                chunk = json.loads(data_str)
                delta = chunk.get("choices", [{}])[0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    accumulated.append(content)
            except Exception:
                continue

        return {"content": "".join(accumulated)}, None
    except Exception as e:
        if _USER_INTERRUPT_FLAG.is_set() or is_user_request_waiting():
            return None, "interrupted_by_user"
        return None, f"stream_error: {e}"
    finally:
        with _ACTIVE_PROACTIVE_HTTP_LOCK:
            _ACTIVE_PROACTIVE_HTTP_RESP = None
        try:
            resp.close()
        except Exception:
            pass

# NOTE ON SEPARATE HTTP CLIENT:
# core/proactive.py maintains an independent streaming HTTP client (query_proactive_model_stream)
# rather than routing through core/llm.py for two reasons:
# 1. Real-time interruptibility: User priority requires holding an active raw socket handle
#    (_ACTIVE_PROACTIVE_HTTP_RESP) that can be closed instantly via abort_active_proactive_call()
#    from the main thread when an interactive query arrives.
# 2. Safety isolation: Proactive background thought generation is strictly non-actionable and
#    forbidden from executing system actions. Using a dedicated streaming client guarantees
#    zero exposure to external calling arguments or function invocation hooks.

def generate_proactive_thought(force=False, category=None):
    """
    Call the local LLM using streaming query without passing any tool parameters.
    Returns (accepted_text, rejection_reason, duration_seconds, chosen_category).
    """
    chosen_category = category if category is not None else random.choice(TOPIC_CATEGORIES)

    # Step 4 check: Before the proactive call starts, check whether a user request is waiting on MODEL_LOCK
    if is_user_request_waiting() or _USER_INTERRUPT_FLAG.is_set():
        logger.info("[Proactive] User request is waiting on model lock; skipping proactive call.")
        return None, "user_request_waiting", 0.0, chosen_category

    recent_lines = get_recent_log_lines(30)
    system_prompt = (
        "You are Buddy, speaking unprompted. "
        "Say one short, natural sentence on any topic you choose. "
        "If you are not sure something is true, say so. "
        "Do not ask for actions. Do not claim to have done anything."
    )
    if recent_lines:
        formatted_history = "\n".join(f"- {line}" for line in recent_lines)
        system_prompt += (
            f"\n\nPreviously spoken statements (do NOT repeat or copy any of these):\n"
            f"{formatted_history}"
        )

    # Step 2: Topic seeding
    user_prompt = f"Topic category: {chosen_category}. Choose a specific subtopic within {chosen_category} and say one short, natural sentence about it."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    _PROACTIVE_GENERATING.set()
    _USER_INTERRUPT_FLAG.clear()

    start_time = time.time()
    try:
        # Check again before locking
        if is_user_request_waiting() or _USER_INTERRUPT_FLAG.is_set():
            elapsed = time.time() - start_time
            return None, "user_request_waiting", elapsed, chosen_category

        with MODEL_LOCK:
            # Check if user arrived while waiting for lock
            if is_user_request_waiting() or _USER_INTERRUPT_FLAG.is_set():
                elapsed = time.time() - start_time
                return None, "user_request_waiting", elapsed, chosen_category

            response_msg, stream_err = query_proactive_model_stream(
                messages=messages,
                max_tokens=MAX_RESPONSE_TOKENS,
                temperature=TEMPERATURE
            )
            if stream_err is not None:
                elapsed = time.time() - start_time
                return None, stream_err, elapsed, chosen_category

        elapsed = time.time() - start_time

        # Check if user arrived while generating (post-hoc discard backup)
        if _USER_INTERRUPT_FLAG.is_set():
            logger.info("[Proactive] Generation was completed but dropped due to user message priority.")
            return None, "interrupted_by_user", elapsed, chosen_category

        if not response_msg:
            return None, "empty_model_response", elapsed, chosen_category

        raw_content = response_msg.get("content", "")
        # Remove any thinking tokens if present
        clean_text = re.sub(r'<think>.*?</think>', '', raw_content, flags=re.DOTALL).strip()
        # Clean quotes
        clean_text = clean_text.strip('\'"')

        # Validation 1: Reject empty output
        if not clean_text:
            return None, "empty_output", elapsed, chosen_category

        # Validation 2: Reject output longer than 300 characters
        if len(clean_text) > MAX_RESPONSE_CHARS:
            return None, f"exceeds_max_chars ({len(clean_text)} > {MAX_RESPONSE_CHARS})", elapsed, chosen_category

        # Validation 3: Step 1, C & D repetition check against recent lines (Rules 1, 2, 3)
        rep_check = check_candidate_repetition(clean_text, recent_lines)
        if not rep_check["is_valid"]:
            return None, rep_check["rejection_reason"], elapsed, chosen_category

        return clean_text, None, elapsed, chosen_category

    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"[Proactive] Model generation error: {e}")
        return None, f"exception: {e}", elapsed, chosen_category
    finally:
        _PROACTIVE_GENERATING.clear()

def deliver_proactive_speech(text):
    """
    Deliver accepted proactive speech across processes to a single speech path.
    First try an HTTP POST to http://127.0.0.1:<hud_port>/api/proactive/message with the text
    and the X-Buddy-Secret authentication header.
    If the HUD answers 200, stop there (the browser speaks).
    Only if the POST fails (HUD not running or unreachable), use voice.tts.speak().
    """
    import urllib.request
    hud_port = get_hud_port()
    try:
        url = f"http://127.0.0.1:{hud_port}/api/proactive/message"
        payload = json.dumps({"message": text}).encode("utf-8")
        secret = get_or_create_proactive_secret()
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "X-Buddy-Secret": secret
            }
        )
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            if resp.status == 200:
                logger.debug(f"[Proactive] Speech delivered to HUD on port {hud_port} via POST 200: {text}")
                return "browser_speechSynthesis"
    except Exception as e:
        logger.debug(f"[Proactive] HUD POST on port {hud_port} unreachable ({e}); falling back to server TTS.")

    # Only if POST fails, use server voice.tts.speak()
    try:
        from voice.tts import speak
        speak(text)
        return "server_tts"
    except Exception as e:
        logger.warning(f"[Proactive] Voice speak error: {e}")
        return "tts_error"

def record_utterance_success(text, dt=None):
    """
    Log the spoken utterance and update state last utterance timestamp and daily counter.
    """
    current_dt = dt if isinstance(dt, datetime) else datetime.now()
    now_ts = current_dt.timestamp()
    today_str = current_dt.strftime("%Y-%m-%d")

    # Append to proactive_log.json with timestamp
    log_entry = append_to_proactive_log(text, timestamp=current_dt.isoformat())

    # Update proactive_state.json atomically under state lock
    with STATE_LOCK:
        state = load_proactive_state()
        state["last_utterance"] = now_ts
        if state.get("daily_count_date") == today_str:
            state["daily_count"] = state.get("daily_count", 0) + 1
        else:
            state["daily_count"] = 1
            state["daily_count_date"] = today_str
        save_proactive_state(state)

    return log_entry

def run_proactive_tick(force_ready=False):
    """
    Single tick execution:
    1. Check condition (or bypass if force_ready)
    2. If not ready, log reason and return
    3. If ready, generate text
    4. If rejected, log rejection reason and return
    5. If accepted, speak, update log, update state
    Logs each tick with its reason: disabled, quiet_hours, recently_active, within_gap, daily_max_reached, or spoken, plus the topic category used.
    """
    chosen_category = random.choice(TOPIC_CATEGORIES)

    if force_ready:
        decision = "ready"
    else:
        decision = evaluate_tick_condition()

    if decision != "ready":
        log_line = f"[Proactive Tick] reason: {decision} | category: {chosen_category}"
        print(log_line, flush=True)
        logger.info(log_line)
        return decision

    # Generate thought
    text, rejection_reason, duration, category_used = generate_proactive_thought(category=chosen_category)
    if rejection_reason is not None:
        log_line = f"[Proactive Tick] reason: rejected ({rejection_reason}) | category: {category_used}"
        print(log_line, flush=True)
        logger.warning(log_line)
        return f"rejected ({rejection_reason})"

    # Deliver and record
    deliver_proactive_speech(text)
    record_utterance_success(text)
    log_line = f"[Proactive Tick] reason: spoken | category: {category_used} | text: \"{text}\""
    print(log_line, flush=True)
    logger.info(log_line)
    return "spoken"

def check_mute_phrase(user_input):
    """
    Check for mute phrases handled before the model.
    Matches whole phrases: 'buddy be quiet' and 'buddy talk again'.
    Returns acknowledgment string or None.
    """
    if not user_input or not isinstance(user_input, str):
        return None

    # Whole phrase match: 'buddy be quiet'
    if re.search(r'\bbuddy\s+be\s+quiet\b', user_input, re.IGNORECASE):
        set_proactive_enabled(False)
        return "I will be quiet, Boss. Proactive mode disabled."

    # Whole phrase match: 'buddy talk again'
    if re.search(r'\bbuddy\s+talk\s+again\b', user_input, re.IGNORECASE):
        set_proactive_enabled(True)
        return "Proactive speaking mode is now active, Boss."

    return None

def notify_user_request_arrived():
    """
    Signal priority for incoming user query over proactive generation.
    Aborts in-flight proactive HTTP call immediately.
    """
    touch_user_activity()
    if _PROACTIVE_GENERATING.is_set():
        logger.info("[Proactive] User interaction arrived during proactive generation; signalling cancellation/drop.")
        _USER_INTERRUPT_FLAG.set()
        abort_active_proactive_call()

def get_tick_seconds():
    """Return effective tick duration in seconds."""
    return TICK_SECONDS

def is_pid_alive(pid):
    """Check if process with given PID is currently alive."""
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        import psutil
        return psutil.pid_exists(pid)
    except Exception:
        try:
            os.kill(pid, 0)
            return True
        except (OSError, SystemError):
            return False

def acquire_scheduler_lock():
    """
    Single scheduler lock: create memory/proactive_scheduler.lock containing owner PID.
    A second process that finds a live owner logs 'scheduler owned by PID X' and does not start its loop.
    """
    current_pid = os.getpid()
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content.isdigit():
                    owner_pid = int(content)
                    if owner_pid != current_pid and is_pid_alive(owner_pid):
                        msg = f"[Proactive Scheduler] scheduler owned by PID {owner_pid}"
                        print(msg, flush=True)
                        logger.info(msg)
                        return False
        except Exception as e:
            logger.warning(f"[Proactive Scheduler] Lock read error: {e}")

    try:
        os.makedirs(MEMORY_DIR, exist_ok=True)
        with open(LOCK_FILE, "w", encoding="utf-8") as f:
            f.write(str(current_pid))
        print(f"[Proactive Scheduler] Scheduler lock acquired by PID {current_pid}", flush=True)

        import atexit
        def _cleanup_lock():
            try:
                if os.path.exists(LOCK_FILE):
                    with open(LOCK_FILE, "r", encoding="utf-8") as rf:
                        if rf.read().strip() == str(current_pid):
                            os.remove(LOCK_FILE)
            except Exception:
                pass
        atexit.register(_cleanup_lock)
        return True
    except Exception as e:
        logger.error(f"[Proactive Scheduler] Lock write error: {e}")
        return False

_SCHEDULER_THREAD = None
_SCHEDULER_LOCK = threading.Lock()

def proactive_scheduler_loop():
    """
    Daemon thread started at startup.
    Calls run_proactive_tick() every tick_seconds (900).
    Started once and loops forever.
    Does nothing when enabled is false, but keeps running so enabling takes effect without restart.
    Mute ('buddy be quiet') sets enabled false; the thread sees it on its next tick.
    """
    logger.info("[Proactive Scheduler] Background scheduler daemon loop started.")
    while True:
        try:
            run_proactive_tick()
        except Exception as e:
            logger.error(f"[Proactive Scheduler] Tick exception: {e}")

        sleep_target = get_tick_seconds()
        slept = 0.0
        while slept < sleep_target:
            time.sleep(min(1.0, sleep_target - slept))
            slept += 1.0
            sleep_target = get_tick_seconds()

def start_proactive_scheduler():
    """Start the background scheduler daemon thread once if lock is acquired."""
    global _SCHEDULER_THREAD
    with _SCHEDULER_LOCK:
        if _SCHEDULER_THREAD is not None and _SCHEDULER_THREAD.is_alive():
            return _SCHEDULER_THREAD

        if not acquire_scheduler_lock():
            return None

        _SCHEDULER_THREAD = threading.Thread(
            target=proactive_scheduler_loop,
            daemon=True,
            name="BuddyProactiveScheduler"
        )
        _SCHEDULER_THREAD.start()
        logger.info("[Proactive Scheduler] Daemon thread initialized and running.")
        return _SCHEDULER_THREAD
