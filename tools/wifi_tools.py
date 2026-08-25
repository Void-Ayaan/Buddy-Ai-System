import subprocess
import re

def check_wifi_signal_quality():
    """Parse netsh wlan show interfaces to get Wi-Fi SSID, Signal %, and speed."""
    try:
        output = subprocess.check_output("netsh wlan show interfaces", shell=True, encoding="cp1252", errors="ignore")
        
        ssid_match = re.search(r"SSID\s*:\s*(.+)", output)
        signal_match = re.search(r"Signal\s*:\s*(\d+)%", output)
        speed_match = re.search(r"Receive rate\s*\(Mbps\)\s*:\s*(\d+)", output)
        
        ssid = ssid_match.group(1).strip() if ssid_match else "Connected Network"
        signal = signal_match.group(1).strip() if signal_match else None
        speed = speed_match.group(1).strip() if speed_match else None
        
        if signal:
            sig_val = int(signal)
            if sig_val > 80:
                quality = "Excellent"
            elif sig_val > 50:
                quality = "Good"
            else:
                quality = "Fair / Weak"

            speed_str = f" at {speed} Mbps" if speed else ""
            return f"Wi-Fi Network '{ssid}' Signal is at {signal}% [{quality}]{speed_str}, Boss!"
        else:
            return "Wi-Fi is active and connected, Boss!"
    except Exception:
        return "Wi-Fi diagnostic error: Ethernet or offline network active, Boss."
