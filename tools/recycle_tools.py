import ctypes

def empty_recycle_bin():
    """Empty Windows Recycle Bin using SHEmptyRecycleBinW API."""
    try:
        # Flags: SHERB_NOCONFIRMATION (0x00000001) | SHERB_NOPROGRESSUI (0x00000002) | SHERB_NOSOUND (0x00000004)
        flags = 0x00000001 | 0x00000002 | 0x00000004
        res = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, flags)
        
        if res == 0:
            return "Windows Recycle Bin emptied cleanly, Boss! Disk space reclaimed."
        else:
            return "Recycle Bin is already empty, Boss!"
    except Exception as e:
        return f"Could not empty Recycle Bin: {e}"
