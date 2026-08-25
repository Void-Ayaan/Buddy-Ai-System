import urllib.parse
from tools.qr_tools import get_local_ip

def initiate_mobile_audio_call(port=5000):
    """
    Buddy Mobile Audio Voice Call Bridge:
    Triggers an audio-only phone call link between your smartphone mic/speaker and Buddy.
    """
    ip = get_local_ip()
    call_url = f"http://{ip}:{port}/phone_call.html"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=240x240&data={urllib.parse.quote(call_url)}&color=00f3ff&bgboundary=0-0-0-0"
    
    response_msg = (
        f"Boss, Mobile Audio Phone Call Bridge initialized!\n\n"
        f"Open this audio call link on your mobile browser:\n{call_url}\n\n"
        f"Or scan the QR code to talk directly to me through your phone microphone & speaker!"
    )
    
    return {
        "text": response_msg,
        "url": call_url,
        "qr_url": qr_url
    }
