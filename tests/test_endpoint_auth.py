import sys
import os
import time
import json
import urllib.request
import urllib.error
import subprocess
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.proactive import get_or_create_proactive_secret

print("=== STARTING ENDPOINT AUTHENTICATION TEST ===", flush=True)

# 1. Start HUD server
env = os.environ.copy()
env["PYTHONUNBUFFERED"] = "1"
server_proc = subprocess.Popen(
    [sys.executable, os.path.join(BASE_DIR, "ui", "server.py")],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    cwd=BASE_DIR,
    env=env
)
threading.Thread(target=lambda: [l for l in server_proc.stdout], daemon=True).start()

# Wait for server to bind port 5000
server_ready = False
for _ in range(30):
    time.sleep(0.5)
    try:
        with urllib.request.urlopen("http://127.0.0.1:5000/api/telemetry", timeout=1) as check_r:
            if check_r.status == 200:
                server_ready = True
                break
    except Exception:
        pass

if not server_ready:
    subprocess.call(["taskkill", "/F", "/T", "/PID", str(server_proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    raise RuntimeError("ui/server.py failed to bind port 5000 within 15 seconds")

valid_secret = get_or_create_proactive_secret()
url = "http://127.0.0.1:5000/api/proactive/message"
payload = json.dumps({"message": "Authorized proactive voice test."}).encode("utf-8")

def send_test_request(name, headers):
    print(f"\n--- {name} ---", flush=True)
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            body = resp.read().decode("utf-8", errors="replace")
            print(f"HTTP Status: {status}")
            print(f"Response Body: {body}")
            return status, body
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP Status: {status}")
        print(f"Response Body: {body}")
        return status, body

# Test 1: With correct secret header
s1, b1 = send_test_request("Test 1: Correct Header (Expected 200)", {
    "Content-Type": "application/json",
    "X-Buddy-Secret": valid_secret
})

# Test 2: Missing secret header
s2, b2 = send_test_request("Test 2: Missing Header (Expected 403)", {
    "Content-Type": "application/json"
})

# Test 3: Wrong secret header
s3, b3 = send_test_request("Test 3: Wrong Header (Expected 403)", {
    "Content-Type": "application/json",
    "X-Buddy-Secret": "invalid_bogus_token_12345"
})

# Clean up server
subprocess.call(["taskkill", "/F", "/T", "/PID", str(server_proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

assert s1 == 200, f"Expected 200, got {s1}"
assert s2 == 403, f"Expected 403, got {s2}"
assert s3 == 403, f"Expected 403, got {s3}"

print("\n=== ALL 3 AUTHENTICATION TESTS PASSED ===", flush=True)
