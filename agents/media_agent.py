from tools.media_tools import volume_up, volume_down, toggle_mute, play_pause, next_track, previous_track
from tools.sound_test_tools import test_speaker_audio

class MediaAgent:
    """AGENT-08: System Volume, Playback Media Controls, and Speaker Diagnostics."""
    def __init__(self):
        self.agent_id = "AGENT-08"
        self.name = "MEDIA-PILOT"

    def vol_up(self):
        return volume_up()

    def vol_down(self):
        return volume_down()

    def mute(self):
        return toggle_mute()

    def test_audio(self):
        return test_speaker_audio()
