import platform
import psutil

def get_hardware_specs():
    """Summarize processor, RAM, OS architecture, and hardware specs."""
    try:
        proc_name = platform.processor() or "AMD64 Processor"
        os_arch = f"{platform.system()} {platform.release()} ({platform.architecture()[0]})"
        ram_total = round(psutil.virtual_memory().total / (1024**3), 1)
        disk_total = round(psutil.disk_usage('C:\\').total / (1024**3), 1)

        return (
            f"Hardware Specs: Running {os_arch} on {proc_name} with "
            f"{ram_total} gigabytes of physical RAM and {disk_total} gigabytes C drive storage, Boss!"
        )
    except Exception as e:
        return f"Could not fetch hardware specs: {e}"
