import winsound
import time

def test_speaker_audio():
    """Play diagnostic audio frequencies to test system speakers."""
    print("\n[ 🔊 TESTING SYSTEM SPEAKERS... ]")
    try:
        # Play 3-frequency ascending chime
        winsound.Beep(523, 200) # C5
        winsound.Beep(659, 200) # E5
        winsound.Beep(784, 300) # G5
        return "Speaker audio diagnostic complete! Sound chimes played successfully, Boss."
    except Exception as e:
        return f"Speaker test error: {e}"
