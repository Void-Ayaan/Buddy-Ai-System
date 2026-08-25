import sounddevice as sd
import numpy as np
import speech_recognition as sr
import io
import wave
import time
import sys

WAKE_WORDS = ["buddy", "hey buddy", "ok buddy", "hello buddy", "budi", "body"]

def listen_for_wake_word(sample_rate=44100, clip_duration=2.5):
    """Listen continuously for wake word 'Hey Buddy' or 'Buddy'."""
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 100
    recognizer.dynamic_energy_threshold = True

    try:
        audio_data = sd.rec(
            int(clip_duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='int16'
        )
        sd.wait()

        max_amp = np.max(np.abs(audio_data))
        if max_amp < 20:
            return False

        # Amplify audio
        gain = 24000.0 / max(max_amp, 1)
        audio_boosted = np.clip(audio_data * gain, -32768, 32767).astype(np.int16)

        wav_io = io.BytesIO()
        with wave.open(wav_io, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_boosted.tobytes())
        wav_io.seek(0)

        with sr.AudioFile(wav_io) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio).lower().strip()

        for wake in WAKE_WORDS:
            if wake in text:
                print(f"\n[ 🔊 WAKE WORD DETECTED: '{text}' -> Waking up Buddy! ]")
                return True

        return False

    except Exception:
        return False

def start_wake_word_loop(on_wake_callback):
    """Continuously poll microphone for wake word until triggered."""
    print("[ WAKE WORD LISTENER ACTIVE: Say 'Hey Buddy' or 'Buddy' to activate... ]")
    while True:
        if listen_for_wake_word():
            on_wake_callback()
            time.sleep(1)
