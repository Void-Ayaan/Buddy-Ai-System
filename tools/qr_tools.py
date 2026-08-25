import socket
import urllib.parse

def get_local_ip():
    """Detect local Wi-Fi / LAN IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

def get_mobile_connect_info(port=5000):
    """Return local IP and QR Code image URL for mobile connection."""
    ip = get_local_ip()
    url = f"http://{ip}:{port}"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={urllib.parse.quote(url)}&color=00f3ff&bgboundary=0-0-0-0"
    
    return {
        "ip": ip,
        "port": port,
        "url": url,
        "qr_url": qr_url
    }
