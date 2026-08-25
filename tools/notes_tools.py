import json
import os

NOTES_FILE = "memory/notes.json"

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_notes(notes):
    os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
    try:
        with open(NOTES_FILE, "w") as f:
            json.dump(notes, f, indent=4)
    except Exception:
        pass

def add_note(note_text):
    text = note_text.strip()
    for prefix in ["add note", "take note", "remind me to", "note down", "add todo", "todo"]:
        if text.lower().startswith(prefix):
            text = text[len(prefix):].strip()

    if not text:
        return "Please specify what you want to note down."

    notes = load_notes()
    notes.append(text)
    save_notes(notes)
    return f"Added note: '{text}', Boss!"

def get_notes():
    notes = load_notes()
    if not notes:
        return "You have no saved notes or to-do items, Boss!"
    
    note_list = "; ".join([f"Note {i+1}: {n}" for i, n in enumerate(notes)])
    return f"Here are your notes: {note_list}."

def clear_notes():
    save_notes([])
    return "All notes have been cleared, Boss!"
