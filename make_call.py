import os
from twilio.rest import Client

# Get environment variables
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
APP_URL = os.environ.get("APP_URL")  # Must be publicly accessible

# Check if all environment variables are set
for name, value in [("SID", TWILIO_ACCOUNT_SID), ("TOKEN", TWILIO_AUTH_TOKEN), ("FROM", TWILIO_PHONE_NUMBER), ("APP_URL", APP_URL)]:
    if not value:
        raise ValueError(f"{name} environment variable is not set!")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

to_number = input("Enter the phone number to call (with country code, e.g., +1XXXXXXXXXX): ")

try:
    call = client.calls.create(
        to=to_number,
        from_=TWILIO_PHONE_NUMBER,
        url=APP_URL  # Twilio fetches instructions from this endpoint
    )
    print(f"Call initiated successfully! Call SID: {call.sid}")
except Exception as e:
    print("Error making the call:", e)