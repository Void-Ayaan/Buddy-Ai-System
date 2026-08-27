import random

EMOTION_STATES = {
    "HAPPY": {
        "badge": "[ Mood: Happy (*) ]",
        "emoji": "😊",
        "prefixes": ["Awesome!", "Great to hear from you, Boss!", "Delighted to help!"],
        "speech_rate": 185
    },
    "LOYAL": {
        "badge": "[ Mood: Loyal Assistant (o7) ]",
        "emoji": "🫡",
        "prefixes": ["At your service, Boss!", "Right away!", "Always here for you, Boss."],
        "speech_rate": 175
    },
    "CYBER_CHILL": {
        "badge": "[ Mood: Cyber-Chill (==) ]",
        "emoji": "😎",
        "prefixes": ["All systems optimal.", "Checked and loaded.", "Got it, Boss."],
        "speech_rate": 170
    },
    "THOUGHTFUL": {
        "badge": "[ Mood: Thoughtful (?) ]",
        "emoji": "🧠",
        "prefixes": ["That's an intriguing question.", "Let me process that carefully.", "Here is my perspective."],
        "speech_rate": 165
    },
    "PLAYFUL": {
        "badge": "[ Mood: Playful (^_^) ]",
        "emoji": "⚡",
        "prefixes": ["Haha, I like your style!", "You got it!", "Let's do this!"],
        "speech_rate": 180
    }
}

CURRENT_MOOD = "LOYAL"

def detect_emotion_from_input(text):
    global CURRENT_MOOD
    text_lower = text.lower().strip()

    if any(p in text_lower for p in ["thank", "great job", "awesome", "good job", "love", "happy", "nice"]):
        CURRENT_MOOD = "HAPPY"
    elif any(p in text_lower for p in ["cool", "chill", "status", "cyber", "mode"]):
        CURRENT_MOOD = "CYBER_CHILL"
    elif any(p in text_lower for p in ["why", "how come", "explain", "think", "what if"]):
        CURRENT_MOOD = "THOUGHTFUL"
    elif any(p in text_lower for p in ["haha", "lol", "joke", "fun", "game"]):
        CURRENT_MOOD = "PLAYFUL"
    else:
        CURRENT_MOOD = "LOYAL"

    return CURRENT_MOOD

def get_current_emotion():
    return EMOTION_STATES.get(CURRENT_MOOD, EMOTION_STATES["LOYAL"])

def format_emotional_response(response_text):
    emotion = get_current_emotion()
    badge = emotion["badge"]
    print(f"\n{badge}")
    return response_text
