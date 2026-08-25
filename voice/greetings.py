import random
import datetime
from memory.memory_manager import load_memory

def get_random_greeting():
    data = load_memory()
    name = data.get("name", "Boss")

    now = datetime.datetime.now()
    hour = now.hour

    if hour < 12:
        time_greeting = "Good morning"
    elif hour < 17:
        time_greeting = "Good afternoon"
    else:
        time_greeting = "Good evening"

    greetings = [
        f"{time_greeting}, {name}! Buddy is online and ready for your command.",
        f"Hello {name}! Systems operational and ready to assist you.",
        f"Buddy at your service, {name}! How can I help you today?",
        f"Welcome back, {name}! All systems are online.",
        f"Greetings, {name}! Local AI model loaded and ready for instructions.",
        f"{time_greeting}, Boss {name}! Ready when you are."
    ]

    return random.choice(greetings)
