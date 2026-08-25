import time
import ctypes
import re

# Win32 Virtual Key Codes
VK_SPACE = 0x20
VK_RETURN = 0x0D

# Key Event Flags
KEYEVENTF_KEYUP = 0x0002

def _press_key(vk_code):
    """Simulate single keydown and keyup event via Win32 user32 API."""
    ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)

def _send_text_keystrokes(text):
    """Send text characters as keyboard strokes to active Windows PIN/Password field."""
    user32 = ctypes.windll.user32
    for char in text:
        # VkKeyScanW maps unicode character to virtual key code
        vk = user32.VkKeyScanW(ord(char))
        if vk != -1:
            vk_code = vk & 0xFF
            shift_state = (vk >> 8) & 0xFF
            
            if shift_state & 1: # Shift key required for uppercase/special char
                user32.keybd_event(0x10, 0, 0, 0) # VK_SHIFT down
                
            user32.keybd_event(vk_code, 0, 0, 0)
            time.sleep(0.03)
            user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)
            
            if shift_state & 1:
                user32.keybd_event(0x10, 0, KEYEVENTF_KEYUP, 0) # VK_SHIFT up
            time.sleep(0.02)

def unlock_windows_pc(prompt_payload):
    """
    Buddy Autonomous Windows PC Unlock Protocol:
    1. Parses password/PIN from payload ("unlock pc 1234", "unlock computer with password myPass").
    2. Presses Space/Enter to wake lock screen and open PIN box.
    3. Types password keystrokes into PIN box.
    4. Presses Enter to unlock PC!
    """
    if not prompt_payload:
        return "Boss, please specify your password or PIN (e.g. 'unlock pc 1234')."

    # Extract password string from command
    password = re.sub(r"^(?:with\s+password|with\s+pin|password|pin)\s+", "", prompt_payload, flags=re.IGNORECASE).strip()
    if not password:
        password = prompt_payload.strip()

    try:
        # Step 1: Press Space key to wake up lock screen and present PIN input box
        _press_key(VK_SPACE)
        time.sleep(0.4)
        _press_key(VK_SPACE)
        time.sleep(0.4)

        # Step 2: Type password keystrokes
        _send_text_keystrokes(password)
        time.sleep(0.2)

        # Step 3: Press Enter key to submit PIN/Password
        _press_key(VK_RETURN)

        return f"Boss, sent unlock sequence with your password to your PC lock screen! Your PC is now unlocking."
    except Exception as e:
        return f"Error executing unlock sequence: {e}"
