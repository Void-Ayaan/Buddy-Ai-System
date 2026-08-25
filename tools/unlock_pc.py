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
    """Send direct Unicode scan code to open PIN/password input box."""
    scan_code = ord(char)
    _send_key_event(0, scan_code, KEYEVENTF_UNICODE)
    time.sleep(0.04)
    _send_key_event(0, scan_code, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP)
    time.sleep(0.04)

def wake_windows_lock_screen():
    """Step 1: Press Space and Enter keys to awaken screen and slide up lock wallpaper."""
    try:
        # Press Space key (VK 0x20)
        _send_key_event(0x20, 0, 0)
        time.sleep(0.06)
        _send_key_event(0x20, 0, KEYEVENTF_KEYUP)
        time.sleep(0.5)

        # Press Enter key (VK 0x0D)
        _send_key_event(0x0D, 0, 0)
        time.sleep(0.06)
        _send_key_event(0x0D, 0, KEYEVENTF_KEYUP)
        time.sleep(0.3)

        return (
            "Boss, I sent the SPACE key sequence to awaken your lock screen!\n\n"
            "The password input box should now be visible on your PC screen.\n"
            "Please reply with your exact password (e.g. 'password 1234' or type your PIN) to log in!"
        )
    except Exception as e:
        return f"Error waking screen: {e}"

def submit_unlock_password(password_text):
    """Step 2: Type exact password into focused PIN box and press Enter."""
    clean_pwd = password_text.strip()
    if not clean_pwd:
        return "Please enter your password (e.g. 'password 1234')."

    try:
        # Ensure focus by sending subtle space backspace
        for ch in clean_pwd:
            _type_character_unicode(ch)

        time.sleep(0.3)

        # Press Enter key to submit login
        _send_key_event(0x0D, 0, 0)
        time.sleep(0.06)
        _send_key_event(0x0D, 0, KEYEVENTF_KEYUP)

        return f"Boss, typed exact password into lock screen and sent ENTER key! Your PC is logging in."
    except Exception as e:
        return f"Error typing password: {e}"

def unlock_windows_pc(prompt_payload):
    """
    Buddy 2-Step Interactive Unlock Engine:
    - If payload is empty -> Step 1: Wakes screen with SPACE key and prompts user for password.
    - If payload contains password -> Step 2: Types exact password and submits ENTER!
    """
    clean_payload = (prompt_payload or "").strip()
    clean_payload = re.sub(r"^(?:with\s+password|with\s+pin|password|pin)\s*", "", clean_payload, flags=re.IGNORECASE).strip()

    if not clean_payload:
        return wake_windows_lock_screen()
    else:
        # Step 1: Wake screen
        wake_windows_lock_screen()
        time.sleep(0.6)
        # Step 2: Type exact password
        return submit_unlock_password(clean_payload)
