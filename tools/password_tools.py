import secrets
import string
import tkinter as tk

def generate_secure_password(length=16):
    """Generate cryptographically secure 16-character password and copy to clipboard."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))

    try:
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()
        root.destroy()
        clip_str = " (Copied to clipboard!)"
    except Exception:
        clip_str = ""

    return f"Generated secure password: {password}{clip_str}, Boss!"
