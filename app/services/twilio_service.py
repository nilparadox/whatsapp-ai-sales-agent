from twilio.rest import Client
from app.core.config import settings

def get_client() -> Client:
    if not settings.twilio_account_sid or not settings.twilio_auth_token:
        raise RuntimeError("Twilio credentials not set (TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN).")
    return Client(settings.twilio_account_sid, settings.twilio_auth_token)

def send_whatsapp(to: str, body: str) -> str:
    """
    Sends a WhatsApp message via Twilio.
    Returns Twilio message SID.
    """
    client = get_client()
    msg = client.messages.create(
        from_=settings.twilio_whatsapp_from,
        to=to,
        body=body
    )
    return msg.sid
