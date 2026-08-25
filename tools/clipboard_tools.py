import tkinter as tk

def read_clipboard():
    """Read text currently saved in Windows Clipboard."""
    try:
        root = tk.Tk()
        root.withdraw()
        text = root.clipboard_get()
        root.destroy()
        if text and text.strip():
            preview = text[:150] + ("..." if len(text) > 150 else "")
            return f"Clipboard text is: {preview}"
        return "Clipboard is currently empty."
    except Exception:
        return "Clipboard is empty or does not contain plain text."

def copy_to_clipboard(text):
    """Copy text to Windows Clipboard."""
    try:
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        root.destroy()
        return f"Copied to clipboard: '{text}'"
    except Exception as e:
        return f"Could not copy to clipboard: {e}"
