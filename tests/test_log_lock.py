import sys
import os
import threading
import json
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.proactive import append_to_proactive_log, LOG_FILE

print("=== STARTING CONCURRENT LOG LOCK TEST (8 THREADS x 50 CALLS = 400 ENTRIES) ===", flush=True)

# 1. Reset log file to empty list
if os.path.exists(LOG_FILE):
    try:
        os.remove(LOG_FILE)
    except Exception:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("[]")

errors = []

def worker(thread_id):
    for i in range(50):
        try:
            append_to_proactive_log(f"Thread {thread_id} message {i}")
            time.sleep(0.005)
        except Exception as e:
            errors.append(f"Thread {thread_id} iteration {i} error: {e}")

threads = [threading.Thread(target=worker, args=(t,)) for t in range(8)]

start_time = time.time()
for t in threads:
    t.start()

for t in threads:
    t.join(timeout=30)
elapsed = time.time() - start_time

print(f"All 8 threads finished in {elapsed:.2f}s", flush=True)
print(f"Logged errors during run: {len(errors)}")

# Verify the file is valid JSON and has 400 entries
assert os.path.exists(LOG_FILE), "Log file was not created"

with open(LOG_FILE, "r", encoding="utf-8") as f:
    entries = json.load(f)

is_valid_json = isinstance(entries, list)
count = len(entries)

print(f"Is valid JSON list:       {is_valid_json}")
print(f"Total entries loaded:     {count}")
print(f"First entry:              {entries[0] if count > 0 else 'None'}")
print(f"Last entry:               {entries[-1] if count > 0 else 'None'}")

assert len(errors) == 0, f"Thread errors occurred: {errors}"
assert is_valid_json, "Expected a JSON list"
assert count == 400, f"Expected exactly 400 entries, found {count}"

print("\n--- LOG LOCK CONCURRENCY TEST RESULT: PASS ---", flush=True)
