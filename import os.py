import os
from twilio.rest import Client

# Environment variables
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_number = os.environ.get("TWILIO_PHONE_NUMBER")
app_url = os.environ.get("APP_URL")  # public URL to /voice endpoint

client = Client(account_sid, auth_token)

to_number = input("Enter the phone number to call (with country code): ")

call = client.calls.create(
    to=to_number,
    from_=twilio_number,
    url=app_url
)

print(f"Call initiated to {to_number}. Call SID: {call.sid}")