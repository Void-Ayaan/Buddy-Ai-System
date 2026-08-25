import threading
import time
import re
import winsound
from voice.tts import speak

def _timer_worker(seconds, label):
    time.sleep(seconds)
    message = f"Timer finished for {label}, Boss!" if label != "timer" else "Timer finished, Boss!"
    print("\n===================================")
    print(f" [ ALARM ]: {message}")
    print("===================================\n")

    # Play audible Windows alarm chimes
    try:
        winsound.Beep(1200, 250)
        winsound.Beep(1600, 350)
        winsound.Beep(2000, 450)
    except Exception:
        pass

    # Speak alert out loud
    speak(message)

def set_timer(seconds, label="timer"):
    thread = threading.Thread(target=_timer_worker, args=(seconds, label), daemon=True)
    thread.start()
    unit = "seconds" if seconds < 120 else "minutes"
    display_time = seconds if seconds < 120 else round(seconds / 60, 1)
    return f"Timer set for {display_time} {unit}."

def parse_timer_command(text):
    text_lower = text.lower().strip()

    # Parse seconds (e.g. "10 seconds", "30 secs")
    sec_match = re.search(r"(\d+)\s*(?:seconds|second|secs|sec)", text_lower)
    if sec_match:
        secs = int(sec_match.group(1))
        label_match = re.search(r"to\s+(.+)$", text_lower)
        label = label_match.group(1).strip() if label_match else "timer"
        return set_timer(secs, label)

    # Parse minutes (e.g. "2 minutes", "5 mins")
    min_match = re.search(r"(\d+)\s*(?:minutes|minute|mins|min)", text_lower)
    if min_match:
        mins = int(min_match.group(1))
        label_match = re.search(r"to\s+(.+)$", text_lower)
        label = label_match.group(1).strip() if label_match else "timer"
        return set_timer(mins * 60, label)

    return set_timer(10, "timer")
