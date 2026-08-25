import os
import sys
import threading
import win32com.client
import pythoncom
import re

WEB_MODE = False

def set_web_mode(enabled=True):
    """Enable or disable Web Mode (mutes server-side TTS so browser Web Speech API speaks cleanly without double speech)."""
    global WEB_MODE
    WEB_MODE = enabled

def speak(text):
    """Speak text using Windows SAPI voice engine (unless muted in Web Mode)."""
    global WEB_MODE

    if WEB_MODE:
        return

    clean_text = clean_spoken_text(text)
    if not clean_text:
        return

    print(f"\nBuddy: {clean_text}\n")

    def _speak_thread(phrase):
        try:
            pythoncom.CoInitialize()
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(phrase)
        except Exception:
            pass

    t = threading.Thread(target=_speak_thread, args=(clean_text,))
    t.start()
    t.join() # Synchronous completion

def clean_spoken_text(text):
    if not text:
        return ""
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'[\*\_~`#\[\]()<>"\']', '', text)
    return text.strip()
