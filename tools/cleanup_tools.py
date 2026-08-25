import os
import shutil

def clean_temp_files():
    """Safely clear Windows user temporary files to free up disk space."""
    temp_dir = os.environ.get("TEMP")
    if not temp_dir or not os.path.exists(temp_dir):
        return "Temp directory not found."

    deleted_files = 0
    reclaimed_bytes = 0

    for root, dirs, files in os.walk(temp_dir):
        for f in files:
            file_path = os.path.join(root, f)
            try:
                size = os.path.getsize(file_path)
                os.remove(file_path)
                deleted_files += 1
                reclaimed_bytes += size
            except Exception:
                pass

    mb_freed = round(reclaimed_bytes / (1024 * 1024), 2)
    return f"System Cleanup complete, Boss! Removed {deleted_files} temporary files and reclaimed {mb_freed} megabytes of disk space."
