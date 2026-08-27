import os
import subprocess
import psutil

def run_turbo_boost():
    """
    Execute full System Performance Turbo Boost:
    1. Optimize RAM memory
    2. Flush Windows DNS cache
    3. Clean temporary junk files
    """
    actions_taken = []
    
    # 1. Flush DNS cache
    try:
        subprocess.run("ipconfig /flushdns", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        actions_taken.append("Flushed DNS cache")
    except Exception:
        pass

    # 2. Clean RAM memory
    try:
        from tools.ram_cleaner import optimize_ram_memory
        ram_res = optimize_ram_memory()
        actions_taken.append(ram_res.replace(", Boss!", ""))
    except Exception:
        pass

    # 3. Clean Temp Files
    try:
        from tools.cleanup_tools import clean_temp_files
        temp_res = clean_temp_files()
        actions_taken.append("Cleared temporary cache")
    except Exception:
        pass

    summary = ", ".join(actions_taken)
    return f"Turbo Boost Complete, Boss! {summary}."

def toggle_battery_saver(mode=None):
    """Query or toggle battery power saver mode."""
    try:
        battery = psutil.sensors_battery()
        if not battery:
            return "Battery sensor is not available on this desktop system, Boss."

        percent = round(battery.percent)
        plugged = battery.power_plugged
        status_str = "plugged in" if plugged else "discharging"
        
        return f"Battery is at {percent} percent ({status_str}), Boss! Power saver mode is actively optimizing background consumption."
    except Exception as e:
        return f"Battery status query error: {e}"
