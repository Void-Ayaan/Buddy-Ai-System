import speech_recognition as sr
import sounddevice as sd
import numpy as np
import io
import wave
import time
import sys

def type_text_to_screen(text):
    """Simulate realistic keyboard typing on screen."""
    sys.stdout.write("[ Voice Typed ]: \"")
    sys.stdout.flush()
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03) # Realistic typing animation
    sys.stdout.write("\"\n\n")
    sys.stdout.flush()

def listen_from_microphone(timeout=4):
    """Record speech from default Windows microphone at 44100Hz, amplify audio, type to screen."""
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 100
    recognizer.dynamic_energy_threshold = True

    sample_rate = 44100
    duration = timeout

    print("\n[ LISTENING NOW... Speak your command clearly! ]")

    try:
        # Record natively from system microphone at 44100Hz
        audio_data = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='int16'
        )

        # ASCII Live visual countdown bar
        for sec in range(duration, 0, -1):
            bar = '#' * (duration - sec + 1) + '-' * (sec - 1)
            sys.stdout.write(f"\r  Recording: [{bar}] {sec}s remaining... ")
            sys.stdout.flush()
            time.sleep(1)

        sd.wait()
        sys.stdout.write("\r  Recording complete! Processing speech...                     \n")
        sys.stdout.flush()

        # Check amplitude level
        max_amp = np.max(np.abs(audio_data))
        if max_amp < 15:
            print("[ No speech detected. Please check microphone volume or type your command. ]\n")
            return ""

        # Normalize audio peak to 24000 (80% full scale) for crisp speech recognition
        gain = 24000.0 / max(max_amp, 1)
        audio_boosted = np.clip(audio_data * gain, -32768, 32767).astype(np.int16)

        # Convert to in-memory WAV at 44100Hz
        wav_io = io.BytesIO()
        with wave.open(wav_io, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2) # 16-bit
            wf.setframerate(sample_rate)
            wf.writeframes(audio_boosted.tobytes())
        wav_io.seek(0)

        # Recognize speech
        with sr.AudioFile(wav_io) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio).strip()

        # Type the recognized speech onto the screen character-by-character like a real keyboard!
        type_text_to_screen(text)
        return text

    except sr.UnknownValueError:
        print("[ Speech was not recognized clearly. Please try speaking again. ]\n")
        return ""
    except sr.RequestError as e:
        print(f"[ Speech recognition network error: {e} ]\n")
        return ""
    except Exception as e:
        print(f"[ Microphone note: {e} ]\n")
        return ""
