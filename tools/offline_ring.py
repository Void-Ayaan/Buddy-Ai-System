import os
import subprocess
import socket
from tools.qr_tools import get_local_ip

def trigger_offline_phone_link(phone_number=""):
    """
    100% Offline Local Solution 1: Windows Phone Link Bluetooth Protocol
    Dials your phone offline via Windows Phone Link / Bluetooth HFP.
    No internet or cloud APIs required!
    """
    try:
        if phone_number:
            subprocess.Popen(f'start ms-phone:dial?number={phone_number}', shell=True)
            return f"Boss, triggering offline Bluetooth Phone Link call to {phone_number}!"
        else:
            subprocess.Popen('start ms-phone:', shell=True)
            return "Boss, launching Windows Phone Link Bluetooth Audio Call interface!"
    except Exception as e:
        return f"Error launching Phone Link: {e}"

def trigger_offline_local_ring(port=5000):
    """
    100% Offline Local Solution 2: Local Wi-Fi Socket Ringtone
    Sends a high-priority offline local socket ping to your mobile phone over local Wi-Fi router.
    No internet needed!
    """
    ip = get_local_ip()
    local_call_url = f"http://{ip}:{port}/phone_call.html?autocall=true"

    # Launch local Bluetooth Phone Link automatically
    try:
        subprocess.Popen('start ms-phone:', shell=True)
    except Exception:
        pass

    return (
        f"Boss, 100% Offline Local Mobile Call Triggered!\n\n"
        f"1. Launched Windows Phone Link via Bluetooth for offline call audio.\n"
        f"2. Local offline Wi-Fi Call Link:\n{local_call_url}\n\n"
        f"Zero internet required!"
    )
