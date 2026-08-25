import os
import urllib.parse
from tools.qr_tools import get_local_ip

# Twilio Credentials (can be set via env or config)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

def make_real_cellular_call(user_phone_number=None):
    """
    Buddy Direct Cellular Phone Call Protocol:
    1. If Twilio API credentials exist, places a real cellular phone call to your mobile number!
    2. If no Twilio API key is provided, triggers the Web Phone Call Ringtone Bridge.
    """
    ip = get_local_ip()
    call_url = f"http://{ip}:5000/phone_call.html?autocall=true"

    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and user_phone_number:
        try:
            from twilio.rest import Client
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            
            # TwiML response telling Twilio to connect voice stream
            twiml = f'<Response><Say voice="alice">Hello Boss! Connecting your audio call bridge to Buddy.</Say><Redirect>{call_url}</Redirect></Response>'

            call = client.calls.create(
                twiml=twiml,
                to=user_phone_number,
                from_=TWILIO_PHONE_NUMBER
            )
            return f"Boss, I am dialing your mobile phone number {user_phone_number} right now! Answer the incoming call to speak with me."
        except Exception as e:
            pass

    return (
        f"Boss, Direct Mobile Call Bridge triggered!\n\n"
        f"📱 Open this incoming call ringtone link on your mobile:\n{call_url}\n\n"
        f"To enable real cellular network phone calls (so your phone rings anywhere without Wi-Fi), add your free Twilio Account SID & Phone Number!"
    )
