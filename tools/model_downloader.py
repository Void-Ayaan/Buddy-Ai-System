import os
import sys
import urllib.request

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "Qwen3-1.7B-Q4_K_M.gguf")

# Reliable Hugging Face Direct Download Link for Qwen GGUF Model
MODEL_URL = "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf"

def download_progress(block_num, block_size, total_size):
    downloaded = block_num * block_size
    if total_size > 0:
        percent = min(100, int((downloaded / total_size) * 100))
        mb_downloaded = downloaded / (1024 * 1024)
        total_mb = total_size / (1024 * 1024)
        sys.stdout.write(f"\r[ Downloading GGUF Model: {percent}% ({mb_downloaded:.1f}/{total_mb:.1f} MB) ]")
        sys.stdout.flush()

def ensure_local_gguf_model():
    """Ensure c:\\buddy\\models\\Qwen3-1.7B-Q4_K_M.gguf exists, auto-downloading if missing."""
    os.makedirs(MODEL_DIR, exist_ok=True)

    if os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) > 100 * 1024 * 1024:
        print(f"[ OK ] Local GGUF Model Present: {MODEL_PATH}")
        return True

    print(f"\n[ Initializing Auto-Download of GGUF LLM Model... ]")
    print(f"Target: {MODEL_PATH}\n")

    try:
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH, reporthook=download_progress)
        print(f"\n\n[ OK ] GGUF Model Downloaded & Ready for Offline AI Inference!\n")
        return True
    except Exception as e:
        print(f"\n[ Warning ] Could not auto-download model: {e}")
        print(f"You can manually place your .gguf model file at: {MODEL_PATH}\n")
        return False

if __name__ == "__main__":
    ensure_local_gguf_model()
