import os
import urllib.parse
from tools.qr_tools import get_local_ip

# Twilio Voice API Credentials (Sign up free at https://www.twilio.com)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "YOUR_TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "YOUR_TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+12345678901")

# YOUR PERSONAL MOBILE PHONE NUMBER TO CALL (e.g. "+919876543210" or "+12345678901")
MY_MOBILE_PHONE_NUMBER = os.getenv("MY_MOBILE_PHONE_NUMBER", "")

def make_real_cellular_call(user_phone_number=None):
    """
    Buddy Real Cellular Network Phone Call Protocol:
    Places a real cellular phone call directly to your mobile phone number.
    Your phone rings in your pocket like a normal incoming phone call!
    """
    target_number = user_phone_number or MY_MOBILE_PHONE_NUMBER
    
    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_ACCOUNT_SID != "YOUR_TWILIO_ACCOUNT_SID" and target_number:
        try:
            try:
                from twilio.rest import Client
            except ImportError:
                return "Twilio package not installed. Installing via pip..."
                
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            ip = get_local_ip()
            call_url = f"http://{ip}:5000/phone_call.html"

            # TwiML response instructing Twilio to read greeting and connect voice stream
            twiml = (
                '<Response>'
                '<Say voice="alice">Hello Boss! Connecting your live audio call bridge to Buddy AI.</Say>'
                '</Response>'
            )

            call = client.calls.create(
                twiml=twiml,
                to=target_number,
                from_=TWILIO_PHONE_NUMBER
            )
            return f"Boss, I am dialing your mobile phone number {target_number} right now! Your phone should be ringing."
        except Exception as e:
            return f"Error placing cellular call: {e}"

    ip = get_local_ip()
    call_url = f"http://{ip}:5000/phone_call.html"
    return (
        f"Boss, to make your mobile phone ring directly with a real cellular phone call:\n\n"
        f"1. Sign up for a free Twilio account at https://www.twilio.com\n"
        f"2. Add your Twilio Account SID, Auth Token & Mobile Phone Number to tools/twilio_call.py!\n\n"
        f"Direct audio call link:\n{call_url}"
    )
