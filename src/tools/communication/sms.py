import os
import dotenv
from twilio.rest import Client

dotenv.load_dotenv()

client = Client(
    os.environ.get("TWILIO_ACCOUNT_SID"), os.environ.get("TWILIO_AUTH_TOKEN")
)

outgoing = os.environ.get("TWILIO_FROM_NUMBER")
user_number = os.environ.get("USER_PHONE_NUMBER")


def send_text(body: str):
    client.messages.create(from_=outgoing, body=body, to=user_number)
