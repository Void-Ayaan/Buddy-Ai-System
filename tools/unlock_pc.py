import time
import ctypes
import re

# Win32 SendInput Structures & Constants
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_ushort),
        ("wParamH", ctypes.c_ushort)
    ]

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("ki", KEYBDINPUT),
        ("mi", MOUSEINPUT),
        ("hi", HARDWAREINPUT)
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("u", INPUT_UNION)
    ]

def _send_key_event(vk=0, scan=0, flags=0):
    """Send low-level hardware SendInput keyboard event to Windows kernel."""
    extra = ctypes.c_ulong(0)
    ii_ = INPUT_UNION()
    ii_.ki = KEYBDINPUT(vk, scan, flags, 0, ctypes.pointer(extra))
    x = INPUT(INPUT_KEYBOARD, ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def _type_character_unicode(char):
    """Send direct Unicode scan code (works on Windows Lock Screen password box)."""
    scan_code = ord(char)
    # Key down unicode
    _send_key_event(0, scan_code, KEYEVENTF_UNICODE)
    time.sleep(0.04)
    # Key up unicode
    _send_key_event(0, scan_code, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP)
    time.sleep(0.04)

def unlock_windows_pc(prompt_payload):
    """
    Buddy Low-Level Hardware Windows PC Unlock Protocol:
    1. Sends Space / Enter key to slide up Windows lock wallpaper.
    2. Pauses 1.2s to let password input field acquire cursor focus.
    3. Types Unicode keystrokes directly via SendInput driver API.
    4. Sends Enter key to log into Windows desktop!
    """
    if not prompt_payload:
        return "Boss, please specify your password or PIN (e.g. 'unlock pc 1234')."

    password = re.sub(r"^(?:with\s+password|with\s+pin|password|pin)\s+", "", prompt_payload, flags=re.IGNORECASE).strip()
    if not password:
        password = prompt_payload.strip()

    try:
        # Step 1: Wake screen & dismiss lock wallpaper (Space key VK 0x20)
        _send_key_event(0x20, 0, 0)
        time.sleep(0.05)
        _send_key_event(0x20, 0, KEYEVENTF_KEYUP)
        time.sleep(0.6)

        # Press Enter key (VK 0x0D) to force PIN box focus
        _send_key_event(0x0D, 0, 0)
        time.sleep(0.05)
        _send_key_event(0x0D, 0, KEYEVENTF_KEYUP)
        
        # Pause to guarantee PIN box acquires input focus
        time.sleep(1.0)

        # Step 2: Type password characters via Unicode SendInput
        for ch in password:
            _type_character_unicode(ch)

        time.sleep(0.3)

        # Step 3: Press Enter key to submit login
        _send_key_event(0x0D, 0, 0)
        time.sleep(0.05)
        _send_key_event(0x0D, 0, KEYEVENTF_KEYUP)

        return f"Boss, low-level SendInput unlock sequence executed for '{password}'! Your PC is logging in."
    except Exception as e:
        return f"Error sending SendInput unlock sequence: {e}"
