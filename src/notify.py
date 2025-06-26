import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

def send_sms(message: str):
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    client.messages.create(
        body=message,
        from_=os.getenv("TWILIO_FROM_NUMBER"),
        to=os.getenv("TWILIO_TO_NUMBER")
    )
    print("✅ SMS sent successfully")
