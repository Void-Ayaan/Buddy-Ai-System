import psutil
import datetime

def get_system_uptime():
    """Calculate system uptime in hours and minutes."""
    try:
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        now = datetime.datetime.now()
        uptime = now - boot_time
        
        hours = int(uptime.total_seconds() // 3600)
        minutes = int((uptime.total_seconds() % 3600) // 60)
        return f"System has been running for {hours} hours and {minutes} minutes, Boss!"
    except Exception as e:
        return f"Uptime calculation error: {e}"

def get_top_processes():
    """List top 3 memory consuming processes."""
    try:
        processes = []
        for p in psutil.process_iter(['name', 'memory_info']):
            try:
                mem = p.info['memory_info'].rss / (1024 * 1024) # MB
                processes.append((p.info['name'], round(mem, 1)))
            except Exception:
                pass
                
        processes.sort(key=lambda x: x[1], reverse=True)
        top3 = processes[:3]
        top_str = ", ".join([f"{name} ({mem}MB)" for name, mem in top3])
        return f"Top memory consuming processes are: {top_str}, Boss!"
    except Exception as e:
        return f"Process check error: {e}"
