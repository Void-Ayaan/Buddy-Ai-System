import os
import sys
import subprocess
import time
import urllib.request
import logging

LLAMAFILE_PORT = 8080
LLAMAFILE_HOST = "127.0.0.1"
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
DEFAULT_GGUF = os.path.join(MODELS_DIR, "Qwen3-1.7B-Q4_K_M.gguf")
LLAMAFILE_EXE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "llamafile.exe")

_server_process = None

def is_llamafile_server_running(port=LLAMAFILE_PORT, timeout=1.5):
    """Check if llamafile server is alive and responding on /v1/models."""
    url = f"http://{LLAMAFILE_HOST}:{port}/v1/models"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Buddy-AI"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status == 200
    except Exception:
        return False

def ensure_llamafile_server_running(model_path=DEFAULT_GGUF, port=LLAMAFILE_PORT, max_wait=30):
    """
    Ensure the llamafile server is running with the specified GGUF model.
    If not already running, spawns llamafile.exe as a background daemon.
    """
    global _server_process

    if is_llamafile_server_running(port=port):
        return True

    if not os.path.exists(LLAMAFILE_EXE):
        logging.error(f"[Llamafile] Executable not found at {LLAMAFILE_EXE}")
        return False

    if not os.path.exists(model_path):
        logging.error(f"[Llamafile] GGUF model not found at {model_path}")
        return False

    logging.info(f"[Llamafile] Starting llamafile server on port {port} with {os.path.basename(model_path)}...")

    cmd = [
        LLAMAFILE_EXE,
        "-m", model_path,
        "--server",
        "--port", str(port),
        "--host", LLAMAFILE_HOST,
        "-c", "2048",
        "--reasoning", "off"
    ]

    try:
        creationflags = 0
        if sys.platform == "win32":
            # CREATE_NO_WINDOW (0x08000000) avoids flashing a console window and keeps daemon alive
            creationflags = 0x08000000

        _server_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags
        )

        start_time = time.time()
        while time.time() - start_time < max_wait:
            time.sleep(1.0)
            if is_llamafile_server_running(port=port, timeout=1.5):
                logging.info(f"[Llamafile] Server successfully started and ready on port {port}!")
                return True

        logging.warning(f"[Llamafile] Server did not respond within {max_wait}s.")
        return False
    except Exception as e:
        logging.exception(f"[Llamafile] Failed to spawn server: {e}")
        return False
