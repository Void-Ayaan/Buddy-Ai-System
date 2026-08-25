import threading
import time
import sys

class ThinkingAnimation:
    def __init__(self, message="Buddy is thinking..."):
        self.message = message
        self.running = False
        self.thread = None

    def _animate(self):
        # Safe cross-platform frames for Windows CMD & PowerShell
        frames = [
            " [=] BUDDY IS THINKING [=]  |  . . . . .",
            " [=] BUDDY IS THINKING [=]  /  o . . . .",
            " [=] BUDDY IS THINKING [=]  -  . o . . .",
            " [=] BUDDY IS THINKING [=]  \\  . . o . .",
            " [=] BUDDY IS THINKING [=]  |  . . . o .",
            " [=] BUDDY IS THINKING [=]  /  . . . . o",
            " [=] BUDDY IS THINKING [=]  -  . . . o .",
            " [=] BUDDY IS THINKING [=]  \\  . . o . .",
            " [=] BUDDY IS THINKING [=]  |  . o . . .",
            " [=] BUDDY IS THINKING [=]  /  o . . . .",
        ]

        CYAN = "\033[96m"
        MAGENTA = "\033[95m"
        BOLD = "\033[1m"
        RESET = "\033[0m"

        idx = 0
        while self.running:
            color = CYAN if (idx // 3) % 2 == 0 else MAGENTA
            frame = frames[idx % len(frames)]
            out_str = f"\r{BOLD}{color}{frame}{RESET}  "
            try:
                sys.stdout.write(out_str)
                sys.stdout.flush()
            except Exception:
                pass
            time.sleep(0.08)
            idx += 1

        try:
            sys.stdout.write("\r" + " " * 65 + "\r")
            sys.stdout.flush()
        except Exception:
            pass

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        try:
            sys.stdout.write("\r" + " " * 65 + "\r")
            sys.stdout.flush()
        except Exception:
            pass

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
