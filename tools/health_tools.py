import psutil
import platform

def run_health_check():
    """Analyze overall system health, memory headroom, and storage."""
    try:
        cpu_cores = psutil.cpu_count(logical=True)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('C:\\')
        
        ram_free_gb = round(ram.available / (1024**3), 1)
        disk_free_gb = round(disk.free / (1024**3), 1)
        
        health_status = "Optimal"
        if ram.percent > 85 or disk.percent > 90:
            health_status = "High Load"

        return (
            f"Laptop Health Status is {health_status}, Boss! "
            f"You have {ram_free_gb} gigabytes of free RAM, {disk_free_gb} gigabytes of free C drive storage, "
            f"and {cpu_cores} logical CPU cores active."
        )
    except Exception as e:
        return f"Health check error: {e}"
