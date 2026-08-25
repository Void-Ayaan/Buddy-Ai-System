import os

def get_desktop_dir():
    """Detect the actual active Windows Desktop path (OneDrive or Standard Desktop)."""
    candidates = [
        os.path.join(os.path.expanduser('~'), 'OneDrive', 'Desktop'),
        os.path.join(os.getenv('USERPROFILE', ''), 'OneDrive', 'Desktop'),
        os.path.join(os.path.expanduser('~'), 'Desktop'),
        os.path.join(os.getenv('USERPROFILE', ''), 'Desktop'),
    ]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    fallback = os.path.join(os.path.expanduser('~'), 'Desktop')
    os.makedirs(fallback, exist_ok=True)
    return fallback

_last_saved_file = os.path.join(get_desktop_dir(), "calculator.py")

def save_code_to_desktop(query):
    """Generate requested code and save file directly to user's Desktop."""
    global _last_saved_file
    desktop_dir = get_desktop_dir()
    query_lower = query.lower()

    if "calculator" in query_lower:
        filename = "calculator.py"
        code = (
            "# Simple Calculator in Python\n"
            "def add(a, b):\n"
            "    return a + b\n\n"
            "def subtract(a, b):\n"
            "    return a - b\n\n"
            "def multiply(a, b):\n"
            "    return a * b\n\n"
            "def divide(a, b):\n"
            "    return a / b if b != 0 else 'Error: Division by zero'\n\n"
            "if __name__ == '__main__':\n"
            "    print('--- Buddy Calculator ---')\n"
            "    print('5 + 10 =', add(5, 10))\n"
            "    print('20 - 4 =', subtract(20, 4))\n"
            "    print('6 * 7 =', multiply(6, 7))\n"
            "    print('50 / 2 =', divide(50, 2))\n"
        )
    else:
        filename = "buddy_script.py"
        code = (
            "# Buddy Assistant Custom Automation Script\n"
            "import os\n"
            "import sys\n\n"
            "def main():\n"
            "    print('Script execution initialized, Boss!')\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        )

    file_path = os.path.join(desktop_dir, filename)
    _last_saved_file = file_path

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        return f"I have written the Python code and saved it directly to your Desktop at {file_path}, Boss!"
    except Exception as e:
        return f"Failed to save code file to desktop: {e}"

def locate_last_saved_file():
    """Return location of last saved desktop file."""
    global _last_saved_file
    if os.path.exists(_last_saved_file):
        return f"Your saved file is located directly on your Desktop at {_last_saved_file}, Boss!"
    return f"The file location is set to {_last_saved_file}, Boss!"
