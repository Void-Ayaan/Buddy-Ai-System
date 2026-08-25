import subprocess
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from voice.wake_word import listen_for_wake_word
from tools.window_bringer import bring_hud_to_front

def run_wake_word_daemon():
    print("=" * 60)
    print("  BUDDY HANDS-FREE WAKE WORD SERVICE ACTIVE")
    print("  Say 'Hey Buddy' -> Launches HUD App Window")
    print("  Say 'Buddy'     -> Overlays HUD in front of all active apps!")
    print("=" * 60 + "\n")

    while True:
        try:
            if listen_for_wake_word():
                print("\n[ WAKE TRIGGER DETECTED! ]")
                # Bring HUD window to front overlay over Instagram/any app!
                bring_hud_to_front()

                # If HUD server is not running, launch launch_hud.bat automatically!
                bat_path = os.path.join(BASE_DIR, "launch_hud.bat")
                subprocess.Popen(f'start "" "{bat_path}"', shell=True)
                time.sleep(3)
        except KeyboardInterrupt:
            print("\nWake Word Daemon stopped.")
            break
        except Exception as e:
            time.sleep(1)

if __name__ == "__main__":
    run_wake_word_daemon()
