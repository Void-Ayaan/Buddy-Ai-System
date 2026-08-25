import json
import os
import re

MEMORY_FILE = "memory/profile.json"

STOPWORDS = {"i", "im", "i'm", "you", "your", "the", "a", "an", "and", "boss", "my", "name", "is", "hello", "hi", "hey", "remember"}

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_memory(key, value):
    data = load_memory()
    data[key] = value
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)
    return f"Got it! I will remember that your {key} is {value}."

def parse_and_save_memory(text):
    text_clean = text.strip()
    text_lower = text_clean.lower()

    if "=" in text:
        try:
            clean = text.replace("remember", "").strip()
            key, val = clean.split("=", 1)
            return save_memory(key.strip(), val.strip())
        except Exception:
            pass

    saved = []

    # Extract name via phrase: "my name is Ansh", "call me Ansh"
    name_match = re.search(r"\b(?:my name is|call me)\s+([a-zA-Z]+)", text_clean, re.IGNORECASE)
    if name_match:
        name = name_match.group(1).capitalize()
        save_memory("name", name)
        saved.append(f"name is {name}")
    else:
        words = [w.strip(",.!") for w in text_clean.split()]
        candidate_names = [w for w in words if w.lower() not in STOPWORDS and w.isalpha()]
        if candidate_names:
            name = candidate_names[0].capitalize()
            save_memory("name", name)
            saved.append(f"name is {name}")

    if "boss" in text_lower:
        save_memory("role", "boss")
        saved.append("role is boss")

    if saved:
        return "Got it! I've remembered that: " + ", and ".join(saved) + "."

    return save_memory("info", text)

def get_memory_summary():
    data = load_memory()
    if not data:
        return ""

    parts = []
    if "name" in data:
        parts.append(f"The user's name is {data['name']}.")
    if "role" in data:
        if data["role"].lower() == "boss":
            parts.append("The user is your boss (you are their loyal AI assistant).")
        else:
            parts.append(f"The user's role is {data['role']}.")

    for k, v in data.items():
        if k not in ["name", "role", "city"]:
            parts.append(f"The user's {k} is {v}.")

    return " ".join(parts)
