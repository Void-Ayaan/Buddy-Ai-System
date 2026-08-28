import os
import sys
import time
import subprocess
import urllib.request
import threading

REPO_DIR = r"c:\buddy"
_upgrader_thread_started = False
_last_upgrade_time = 0

def is_internet_connected():
    """Fast non-blocking internet connection check."""
    try:
        req = urllib.request.Request("http://www.google.com", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            return resp.status == 200
    except Exception:
        pass
    return False

def check_and_run_auto_upgrade(force=False):
    """
    Automatic GitHub Self-Upgrader:
    1. Verifies internet connectivity.
    2. Checks remote GitHub repository for new commits (git fetch origin main).
    3. Pulls latest updates automatically (git pull origin main).
    4. Upgrades missing requirements.txt dependencies.
    """
    global _last_upgrade_time
    now = time.time()

    # Don't check more than once every 10 minutes unless force=True
    if not force and (now - _last_upgrade_time < 600):
        return "Auto-upgrader checked recently, Boss. System is running the latest build."

    _last_upgrade_time = now

    if not is_internet_connected():
        return "No internet connection detected, Boss. Auto-upgrader is waiting for network online state."

    actions_taken = []
    try:
        # Step 1: Fetch remote changes
        fetch_res = subprocess.run(
            ["git", "fetch", "origin", "main"],
            cwd=REPO_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )

        # Step 2: Compare local HEAD with origin/main
        local_hash = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        ).stdout.strip()

        remote_hash = subprocess.run(
            ["git", "rev-parse", "origin/main"],
            cwd=REPO_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        ).stdout.strip()

        if force or (local_hash and remote_hash and local_hash != remote_hash):
            # Step 3: Pull remote commits
            pull_res = subprocess.run(
                ["git", "pull", "origin", "main", "--no-rebase"],
                cwd=REPO_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=15
            )
            if "Already up to date" in pull_res.stdout:
                actions_taken.append("GitHub repository code is up to date")
            else:
                actions_taken.append("Pulled latest code updates from GitHub (main)")

            # Step 4: Upgrade requirements if present
            req_file = os.path.join(REPO_DIR, "requirements.txt")
            if os.path.exists(req_file):
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", req_file, "--quiet"],
                    cwd=REPO_DIR,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                actions_taken.append("Updated python package dependencies")
        else:
            actions_taken.append("System is fully synchronized with latest GitHub build")

        summary = ", ".join(actions_taken)
        return f"Automatic Self-Upgrade Complete, Boss! {summary}."

    except Exception as e:
        return f"Auto-upgrade check status: {e}"

def _background_upgrader_loop():
    """Background daemon loop that periodically checks for GitHub updates when online."""
    time.sleep(10) # Initial boot delay
    while True:
        try:
            if is_internet_connected():
                check_and_run_auto_upgrade(force=False)
        except Exception:
            pass
        time.sleep(600) # Check every 10 minutes

def start_auto_upgrader_background_daemon():
    """Launch non-blocking background daemon thread for auto self-upgrading."""
    global _upgrader_thread_started
    if not _upgrader_thread_started:
        _upgrader_thread_started = True
        t = threading.Thread(target=_background_upgrader_loop, daemon=True)
        t.start()
        print("[ AUTO-UPGRADER DAEMON: Background Internet Self-Upgrader Active ]")
