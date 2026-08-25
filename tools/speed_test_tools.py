import requests
import time

def run_quick_speed_test():
    """Measure download latency and estimated internet download speed."""
    url = "https://speed.cloudflare.com/__down?bytes=1000000" # 1MB test file
    print("\n[ RUNNING FAST INTERNET SPEED TEST... ]")

    try:
        start_time = time.time()
        res = requests.get(url, timeout=8)
        end_time = time.time()

        if res.status_code == 200:
            duration = max(end_time - start_time, 0.01)
            size_mb = 1.0 # 1 MB
            speed_mbps = round((size_mb * 8) / duration, 2)
            ping_ms = int(duration * 100)

            return f"Speed test complete, Boss! Estimated download speed is {speed_mbps} Megabits per second with {ping_ms} ms ping latency."
    except Exception:
        pass

    return "Could not run speed test right now. Please check your internet connection."
