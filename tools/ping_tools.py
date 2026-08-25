import socket
import time

def check_ping_latency(host="8.8.8.8", port=53, count=3):
    """Measure network TCP ping latency to target host in milliseconds."""
    latencies = []

    for _ in range(count):
        start = time.time()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            sock.connect((host, port))
            sock.close()
            latency = (time.time() - start) * 1000 # ms
            latencies.append(latency)
        except Exception:
            pass
        time.sleep(0.1)

    if latencies:
        avg_ping = round(sum(latencies) / len(latencies), 1)
        if avg_ping < 30:
            quality = "Ultra-Fast (Gaming Grade)"
        elif avg_ping < 80:
            quality = "Good & Stable"
        else:
            quality = "High Latency"

        return f"Network Ping to DNS ({host}): {avg_ping} ms [{quality}], Boss!"
    else:
        return f"Ping measurement failed, host {host} unreachable, Boss."
