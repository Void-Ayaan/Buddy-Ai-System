import os
import subprocess
import webbrowser
import datetime
import ctypes

APP_MAPPINGS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "paint": "mspaint.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "my computer": "explorer.exe",
    "task manager": "taskmgr.exe",
    "taskmgr": "taskmgr.exe",
    "cmd": "cmd.exe",
    "command prompt": "cmd.exe",
    "terminal": "wt.exe",
    "settings": "start ms-settings:",
    "control panel": "control.exe",
    "snipping tool": "snippingtool.exe",
    "screenshot": "snippingtool.exe",
    "edge": "msedge.exe",
    "msedge": "msedge.exe",
    "vscode": "code",
    "vs code": "code",
    "code": "code",
    "spotify": "spotify.exe",
}

APP_EXE_MAPPINGS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "edge": "msedge.exe",
    "paint": "mspaint.exe",
    "explorer": "explorer.exe",
    "task manager": "taskmgr.exe",
    "spotify": "spotify.exe",
    "code": "Code.exe",
    "vscode": "Code.exe"
}

def fix_microphone():
    """Open Windows Microphone Settings and Sound Control Panel to help unmute the microphone."""
    try:
        os.system("start ms-settings:privacy-microphone")
        os.system("start mmsys.cpl")
        return "Opening Windows Microphone Settings and Sound Panel to check microphone access."
    except Exception as e:
        return f"Could not open settings: {e}"

def trigger_dictation():
    """Trigger Windows built-in Voice Dictation toolbar (Win + H)."""
    try:
        VK_LWIN = 0x5B
        VK_H = 0x48
        ctypes.windll.user32.keybd_event(VK_LWIN, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_H, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_H, 0, 2, 0)
        ctypes.windll.user32.keybd_event(VK_LWIN, 0, 2, 0)
        return "Activated Windows Voice Dictation (Win + H)."
    except Exception as e:
        return f"Dictation trigger error: {e}"

def get_current_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')}."

def get_current_date():
    now = datetime.datetime.now()
    return f"Today is {now.strftime('%A, %B %d, %Y')}."

def get_system_info():
    info_parts = []
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        info_parts.append(f"Laptop CPU usage is at {int(cpu)} percent, and RAM usage is at {int(ram)} percent.")

        battery = psutil.sensors_battery()
        if battery:
            percent = int(battery.percent)
            plugged = "plugged in" if battery.power_plugged else "on battery"
            info_parts.append(f"Battery is at {percent} percent ({plugged}).")
    except Exception:
        info_parts.append("Laptop performance is operating smoothly.")

    return " ".join(info_parts)

def open_chrome():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if os.path.exists(chrome_path):
        os.startfile(chrome_path)
        return "Opening Chrome"
    webbrowser.open("https://www.google.com")
    return "Opening Chrome"

def open_website(url, name="website"):
    if not url.startswith("http"):
        url = f"https://{url}"
    webbrowser.open(url)
    return f"Opening {name}"

def open_app(app_name):
    app_lower = app_name.lower().strip()

    if app_lower in ["chrome", "google chrome"]:
        return open_chrome()

    if app_lower in APP_MAPPINGS:
        target = APP_MAPPINGS[app_lower]
        try:
            if target.startswith("start "):
                os.system(target)
            else:
                subprocess.Popen(target, shell=True)
            return f"Opening {app_name.capitalize()}"
        except Exception as e:
            return f"Could not open {app_name}: {e}"

    try:
        subprocess.Popen(f"start {app_lower}", shell=True)
        return f"Opening {app_name.capitalize()}"
    except Exception:
        return f"Attempted to open {app_name}."

def close_app(app_name=None):
    if not app_name or app_name.lower().strip() in ["it", "window", "app", "this"]:
        VK_MENU = 0x12
        VK_F4 = 0x73
        ctypes.windll.user32.keybd_event(VK_MENU, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_F4, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_F4, 0, 2, 0)
        ctypes.windll.user32.keybd_event(VK_MENU, 0, 2, 0)
        return "Closed active window."

    app_clean = app_name.lower().strip()
    exe_name = APP_EXE_MAPPINGS.get(app_clean, f"{app_clean}.exe")

    try:
        subprocess.run(f"taskkill /f /im {exe_name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"Closed {app_name.capitalize()}."
    except Exception:
        return f"Closed {app_name}."

def minimize_window():
    """Minimize active window reliably via Win32 API ShowWindow / keybd_event."""
    try:
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        if hwnd:
            # SW_MINIMIZE = 6
            user32.ShowWindow(hwnd, 6)
            return "Minimized window."
    except Exception:
        pass

    VK_LWIN = 0x5B
    VK_DOWN = 0x28
    ctypes.windll.user32.keybd_event(VK_LWIN, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_DOWN, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_DOWN, 0, 2, 0)
    ctypes.windll.user32.keybd_event(VK_LWIN, 0, 2, 0)
    return "Minimized window."

def minimize_all_windows():
    """Minimize all windows / show desktop via Win32 keybd_event (Win + D)."""
    try:
        VK_LWIN = 0x5B
        VK_D = 0x44
        ctypes.windll.user32.keybd_event(VK_LWIN, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_D, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_D, 0, 2, 0)
        ctypes.windll.user32.keybd_event(VK_LWIN, 0, 2, 0)
        return "Minimized all windows and showing desktop, Boss!"
    except Exception as e:
        return f"Could not minimize all windows: {e}"
