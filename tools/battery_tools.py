import psutil

def get_battery_details():
    """Get battery percentage, charging state, and estimated time remaining."""
    try:
        battery = psutil.sensors_battery()
        if not battery:
            return "No battery detected. Laptop is running on direct AC power, Boss!"

        percent = int(battery.percent)
        plugged = "plugged in and charging" if battery.power_plugged else "running on battery"
        
        secs_left = battery.secsleft
        if secs_left == psutil.POWER_TIME_UNLIMITED or secs_left < 0:
            time_str = "fully charged or plugged in."
        else:
            hrs = secs_left // 3600
            mins = (secs_left % 3600) // 60
            time_str = f"with approximately {hrs} hours and {mins} minutes remaining."

        return f"Battery is at {percent} percent, {plugged}, {time_str}"
    except Exception as e:
        return f"Could not fetch battery details: {e}"
