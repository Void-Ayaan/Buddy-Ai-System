import ctypes
import time

SW_RESTORE = 9
SW_MAXIMIZE = 3
HWND_TOPMOST = -1
HWND_NOTOPMOST = -2
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_SHOWWINDOW = 0x0040

def bring_hud_to_front():
    """Find Buddy HUD window and force it to overlay on top of all active windows in Maximized Full Screen."""
    user32 = ctypes.windll.user32

    def enum_windows_callback(hwnd, extra):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                title_buffer = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, title_buffer, length + 1)
                title = title_buffer.value
                if "BUDDY" in title.upper() or "127.0.0.1:5000" in title:
                    # Maximize Full Screen
                    user32.ShowWindow(hwnd, SW_MAXIMIZE)
                    # Force window to top-most z-order overlay
                    user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
                    user32.SetForegroundWindow(hwnd)
                    time.sleep(0.1)
                    # Revert to normal z-order so user can interact normally
                    user32.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
                    return False
        return True

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    user32.EnumWindows(EnumWindowsProc(enum_windows_callback), 0)
