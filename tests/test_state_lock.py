import sys
import os
import threading
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.proactive import (
    load_proactive_state,
    save_proactive_state,
    touch_user_activity,
    set_proactive_enabled,
    record_utterance_success,
    check_mute_phrase,
    STATE_FILE
)

print("=== STARTING STATE LOCK CONCURRENCY TEST (50 ITERATIONS) ===", flush=True)

# Initialize state to enabled
set_proactive_enabled(True)

stop_ticks = threading.Event()
tick_count = 0
errors = []

def tick_worker():
    global tick_count
    while not stop_ticks.is_set():
        try:
            touch_user_activity()
            record_utterance_success(f"Concurrent tick statement {tick_count}")
            tick_count += 1
            time.sleep(0.01)
        except Exception as e:
            errors.append(f"Tick error: {e}")

# Start concurrent background tick thread
t = threading.Thread(target=tick_worker, daemon=True)
t.start()

# 50 iterations calling 'buddy be quiet' and checking state
for i in range(1, 51):
    # Set to true briefly, then call mute phrase
    set_proactive_enabled(True)
    mute_ack = check_mute_phrase("buddy be quiet")
    assert mute_ack is not None, f"Failed to match mute phrase at iteration {i}"
    st = load_proactive_state()
    assert st.get("enabled") is False, f"Iteration {i}: expected enabled=False, got {st.get('enabled')}"

stop_ticks.set()
t.join(timeout=2.0)

final_state = load_proactive_state()
print(f"Total concurrent ticks recorded: {tick_count}")
print(f"Total concurrency errors:        {len(errors)}")
print(f"Final state file contents:       {final_state}")
print(f"Final enabled value:             {final_state.get('enabled')}")
assert len(errors) == 0, f"Errors occurred: {errors}"
assert final_state.get("enabled") is False, f"Expected final enabled=False, got {final_state.get('enabled')}"

print("\n--- STATE LOCK TEST RESULT: PASS ---")
