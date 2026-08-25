import os
import shutil
import glob
from pathlib import Path

# Category extensions for organizing folders
FILE_CATEGORIES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".epub"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv"],
    "Audio": [".mp3", ".wav", ".flac", ".m4a", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso"],
    "Executables": [".exe", ".msi", ".bat", ".cmd", ".ps1"]
}

USER_PROFILE = os.environ.get("USERPROFILE", "C:\\Users\\Default")
DESKTOP_PATH = os.path.join(USER_PROFILE, "Desktop")
DOWNLOADS_PATH = os.path.join(USER_PROFILE, "Downloads")
DOCUMENTS_PATH = os.path.join(USER_PROFILE, "Documents")

def resolve_path(path_str):
    path_clean = path_str.strip().strip("'\"")
    path_lower = path_clean.lower()
    
    if path_lower in ["desktop", "my desktop"]:
        return DESKTOP_PATH
    if path_lower in ["downloads", "my downloads"]:
        return DOWNLOADS_PATH
    if path_lower in ["documents", "my documents"]:
        return DOCUMENTS_PATH
        
    return os.path.abspath(path_clean)

def organize_folder(folder_path="downloads"):
    target_dir = resolve_path(folder_path)

    if not os.path.exists(target_dir):
        return f"Folder not found: {target_dir}"

    moved_count = 0
    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        if os.path.isfile(item_path):
            ext = os.path.splitext(item)[1].lower()
            if not ext:
                continue

            for category, ext_list in FILE_CATEGORIES.items():
                if ext in ext_list:
                    cat_dir = os.path.join(target_dir, category)
                    os.makedirs(cat_dir, exist_ok=True)
                    dest_path = os.path.join(cat_dir, item)
                    try:
                        shutil.move(item_path, dest_path)
                        moved_count += 1
                    except Exception:
                        pass
                    break

    folder_name = os.path.basename(target_dir)
    return f"Organized {moved_count} files in {folder_name} into categorized folders, Boss!"

def move_file(source, destination):
    src = resolve_path(source)
    dst = resolve_path(destination)

    if not os.path.exists(src):
        return f"Source file not found: {source}"

    try:
        shutil.move(src, dst)
        return f"Moved {os.path.basename(src)} to {destination}."
    except Exception as e:
        return f"Failed to move file: {e}"

def copy_file(source, destination):
    src = resolve_path(source)
    dst = resolve_path(destination)

    if not os.path.exists(src):
        return f"Source file not found: {source}"

    try:
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            if os.path.isdir(dst):
                shutil.copy2(src, dst)
            else:
                shutil.copy2(src, dst)
        return f"Copied {os.path.basename(src)} to {destination}."
    except Exception as e:
        return f"Failed to copy file: {e}"

def delete_file(file_path):
    target = resolve_path(file_path)

    if not os.path.exists(target):
        return f"File or folder not found: {file_path}"

    try:
        if os.path.isdir(target):
            shutil.rmtree(target)
        else:
            os.remove(target)
        return f"Deleted {os.path.basename(target)}."
    except Exception as e:
        return f"Failed to delete {file_path}: {e}"

def find_file(filename, search_dir="desktop"):
    target_dir = resolve_path(search_dir)
    found_files = []

    try:
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if filename.lower() in file.lower():
                    found_files.append(os.path.join(root, file))
                    if len(found_files) >= 3:
                        break
            if len(found_files) >= 3:
                break
    except Exception:
        pass

    if found_files:
        matches = ", ".join([os.path.basename(f) for f in found_files])
        return f"Found matching files: {matches}."
    return f"No files matching '{filename}' were found in {search_dir}."
