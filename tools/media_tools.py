import ctypes

# Windows Virtual Key Codes for Media
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_PLAY_PAUSE = 0xCD

def send_key(code):
    ctypes.windll.user32.keybd_event(code, 0, 0, 0)
    ctypes.windll.user32.keybd_event(code, 0, 2, 0)

def volume_up():
    for _ in range(5):
        send_key(VK_VOLUME_UP)
    return "Increased volume."

def volume_down():
    for _ in range(5):
        send_key(VK_VOLUME_DOWN)
    return "Decreased volume."

def toggle_mute():
    send_key(VK_VOLUME_MUTE)
    return "Muted or unmuted audio."

def play_pause():
    send_key(VK_MEDIA_PLAY_PAUSE)
    return "Toggled media playback."

def next_track():
    send_key(VK_MEDIA_NEXT_TRACK)
    return "Playing next track."

def previous_track():
    send_key(VK_MEDIA_PREV_TRACK)
    return "Playing previous track."
