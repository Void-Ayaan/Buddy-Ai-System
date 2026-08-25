import socket
import requests
import subprocess

def get_network_info():
    """Get Local IP, Public IP, and Ping Status."""
    info = []

    # Local IP
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        info.append(f"Local IP address is {local_ip}.")
    except Exception:
        pass

    # Public IP
    try:
        res = requests.get("https://api.ipify.org?format=json", timeout=3)
        if res.status_code == 200:
            public_ip = res.json().get("ip")
            info.append(f"Public IP address is {public_ip}.")
    except Exception:
        info.append("Could not fetch public IP.")

    # Internet Connection Ping Test
    try:
        output = subprocess.check_output("ping -n 1 8.8.8.8", shell=True).decode()
        if "TTL=" in output or "bytes=" in output:
            info.append("Internet connection is online and stable, Boss!")
        else:
            info.append("Internet connection seems weak or offline.")
    except Exception:
        info.append("Internet ping test failed.")

    return " ".join(info)
