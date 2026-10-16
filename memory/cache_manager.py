import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_FILE = os.path.join(BASE_DIR, "memory", "cache.json")

# Strict exact static greetings ONLY. Never cache compound questions or dynamic queries.
ALLOWED_CACHE_KEYS = {"hello", "hi", "hey"}

INTRO_PATTERNS = [
    "i am buddy",
    "your ai assistant",
    "how can i assist you today",
    "i am online and ready to help",
    "warming up",
    "status code",
    "error",
    "i understand, boss",
    "saved this context",
    "how would you like us to proceed",
    "executing protocol"
]

def normalize_query(query):
    """Normalize input query for consistent cache lookup."""
    query = query.lower().strip()
    query = re.sub(r'[^\w\s]', '', query) # Remove punctuation
    query = re.sub(r'\s+', ' ', query)    # Normalize spaces
    return query

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def is_generic_intro(text):
    if not text:
        return True
    lower = text.lower()
    return any(p in lower for p in INTRO_PATTERNS)

def get_cached_response(query):
    key = normalize_query(query)
    # Only allow caching for strict simple static greetings, never dynamic conversational reasoning
    if key not in ALLOWED_CACHE_KEYS:
        return None

    cache = load_cache()
    if key in cache:
        res = cache[key]
        if res and not is_generic_intro(res):
            return res
    return None

def save_cached_response(query, response):
    key = normalize_query(query)

    # Never cache dynamic answers, errors, fallbacks, or conversational turns
    if key not in ALLOWED_CACHE_KEYS:
        return

    if not response or is_generic_intro(response) or any(p in response.lower() for p in ["opening", "closed", "minimized"]):
        return

    cache = load_cache()
    cache[key] = response

    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=4)
    except Exception:
        pass
