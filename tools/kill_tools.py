import psutil

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
