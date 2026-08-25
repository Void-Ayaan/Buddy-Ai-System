import os
import ctypes

def lock_pc():
    """Lock the Windows workstation instantly."""
    try:
        ctypes.windll.user32.LockWorkStation()
        return "Locking PC now, Boss!"
    except Exception as e:
        return f"Could not lock PC: {e}"

def sleep_pc():
    """Put PC to sleep."""
    try:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Putting PC to sleep, Boss!"
    except Exception as e:
        return f"Could not sleep PC: {e}"

def shutdown_pc(seconds=10):
    """Initiate safe shutdown timer."""
    try:
        os.system(f"shutdown /s /t {seconds}")
        return f"Shutdown initiated! PC will turn off in {seconds} seconds. Say 'cancel shutdown' to abort."
    except Exception as e:
        return f"Shutdown error: {e}"

def restart_pc(seconds=10):
    """Initiate restart timer."""
    try:
        os.system(f"shutdown /r /t {seconds}")
        return f"Restart initiated! PC will restart in {seconds} seconds."
    except Exception as e:
        return f"Restart error: {e}"

def cancel_shutdown():
    """Cancel pending shutdown/restart."""
    try:
        os.system("shutdown /a")
        return "Shutdown cancelled successfully, Boss!"
    except Exception as e:
        return f"Could not cancel shutdown: {e}"
