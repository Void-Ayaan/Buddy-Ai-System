import psutil

def run_buddy_system_scan():
    """Run Buddy system scan diagnostic readout."""
    try:
        cpu = int(psutil.cpu_percent(interval=0.1))
        ram = int(psutil.virtual_memory().percent)
        disk = psutil.disk_usage('C:\\')
        disk_free_gb = round(disk.free / (1024**3), 1)

        return f"Buddy System Diagnostic complete, Boss! CPU is running at {cpu} percent, RAM is at {ram} percent, and C drive has {disk_free_gb} gigabytes free."
    except Exception as e:
        return f"System scan error: {e}"
