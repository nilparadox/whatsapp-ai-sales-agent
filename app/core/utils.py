import re

BOOKING_KEYWORDS = {
    "book", "booking", "buy", "order", "confirm", "purchase", "schedule", "install", "delivery"
}

def normalize_whatsapp_from(raw_from: str) -> str:
    """
    Twilio/WhatsApp format should look like: 'whatsapp:+919999999999'
    We normalize common messy inputs (spaces, missing '+').
    """
    s = (raw_from or "").strip()
    s = re.sub(r"\s+", "", s)  # remove all spaces
    if s.startswith("whatsapp:"):
        rest = s[len("whatsapp:"):]
        if rest and not rest.startswith("+"):
            rest = "+" + rest
        return "whatsapp:" + rest
    # if someone sends only digits
    if s and s[0].isdigit():
        if not s.startswith("+"):
            s = "+" + s
        return "whatsapp:" + s
    return s

def detect_status(message: str) -> str:
    m = (message or "").lower()
    for kw in BOOKING_KEYWORDS:
        if kw in m:
            return "BOOKING"
    # if message exists but no booking intent
    return "INQUIRY"
