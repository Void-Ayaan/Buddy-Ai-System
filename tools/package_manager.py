import os
import sys
import subprocess

REQUIREMENTS_FILE = "requirements.txt"

def ensure_package_in_requirements(package_name):
    """Automatically append newly installed package to requirements.txt if not already listed."""
    if not os.path.exists(REQUIREMENTS_FILE):
        open(REQUIREMENTS_FILE, "w").close()

    try:
        with open(REQUIREMENTS_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        pkg_lower = package_name.lower().split("=")[0].split(">")[0].split("<")[0].strip()
        existing_pkgs = [line.strip().lower().split("=")[0].split(">")[0].split("<")[0].strip() for line in lines if line.strip() and not line.startswith("#")]

        if pkg_lower not in existing_pkgs:
            with open(REQUIREMENTS_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n{package_name}")
            print(f"[ PACKAGE MANAGER: Added '{package_name}' to requirements.txt ]")
            return True
    except Exception as e:
        print(f"[ Package Manager Warning: {e} ]")
    return False

def install_and_record_package(package_name):
    """Install package via pip and automatically record it in requirements.txt."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        ensure_package_in_requirements(package_name)
        return True
    except Exception as e:
        print(f"[ Failed to install package {package_name}: {e} ]")
        return False
