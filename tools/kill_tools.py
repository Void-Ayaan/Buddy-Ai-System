import os
import psutil

# Safe list of common user applications that can be terminated
TARGET_USER_APPS = [
    "chrome.exe", "msedge.exe", "firefox.exe", "brave.exe", "opera.exe",
    "notepad.exe", "vlc.exe", "calculator.exe", "spotify.exe", "slack.exe",
    "discord.exe", "steam.exe", "wordpad.exe", "mspaint.exe", "acroctr.exe",
    "adobe.exe", "excel.exe", "winword.exe", "powerpnt.exe"
]

# System critical processes to NEVER kill under any circumstances
CRITICAL_SYSTEM_PROCESSES = [
    "explorer.exe", "svchost.exe", "csrss.exe", "smss.exe", "wininit.exe",
    "services.exe", "lsass.exe", "winlogon.exe", "spoolsv.exe", "dwm.exe",
    "ctfmon.exe", "taskhostw.exe", "system", "idle", "python.exe", "pythonw.exe",
    "cmd.exe", "powershell.exe", "wt.exe", "code.exe"
]

def kill_named_process(process_name):
    """Terminate running processes matching given process name."""
    if not process_name:
        return "Please specify process name to close, Boss."

    proc_query = process_name.lower().strip().replace(".exe", "")
    killed_count = 0

    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                pname = proc.info['name'].lower()
                if any(sys_p in pname for sys_p in CRITICAL_SYSTEM_PROCESSES):
                    continue
                if proc_query in pname:
                    proc.kill()
                    killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if killed_count > 0:
            return f"Successfully terminated {killed_count} instances of {process_name}, Boss!"
        else:
            return f"No active process matching '{process_name}' was found running, Boss."
    except Exception as e:
        return f"Process termination error: {e}"

def kill_all_user_processes():
    """Safely terminate all non-essential user background applications."""
    my_pid = os.getpid()
    killed_apps = set()
    total_killed = 0

    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['pid'] == my_pid:
                    continue

                pname = proc.info['name'].lower()

                # Skip system critical processes & terminals
                if any(sys_p in pname for sys_p in CRITICAL_SYSTEM_PROCESSES):
                    continue

                # Kill known target user applications
                if pname in TARGET_USER_APPS:
                    proc.kill()
                    killed_apps.add(pname.replace(".exe", "").capitalize())
                    total_killed += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if total_killed > 0:
            app_list = ", ".join(list(killed_apps)[:5])
            return f"Successfully terminated {total_killed} processes ({app_list}), Boss!"
        else:
            return "No non-essential user applications are currently running to kill, Boss."
    except Exception as e:
        return f"Kill all processes error: {e}"
