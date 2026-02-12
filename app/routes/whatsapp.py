from fastapi import APIRouter, Form, Query, HTTPException
from fastapi.responses import PlainTextResponse
from loguru import logger

from app.core.utils import normalize_whatsapp_from, detect_status
from app.services.ai_service import generate_reply
from app.services.lead_service import upsert_lead
from app.services.key_service import get_key
from app.services.message_service import add_message, get_recent_messages
from app.db.database import SessionLocal

router = APIRouter()

@router.post("/whatsapp")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    bid: str = Query(default="default"),
    key: str = Query(default="")
):
    business_id = (bid or "default").strip()

    expected = get_key(business_id)
    if expected and key != expected:
        raise HTTPException(status_code=401, detail="Invalid key")

    phone = normalize_whatsapp_from(From)
    status = detect_status(Body)

    logger.info(f"[{business_id}] Message from {phone}: {Body} | status={status}")

    db = SessionLocal()
    try:
        # Store user message
        add_message(db, business_id=business_id, phone=phone, role="user", content=Body)

        # Load last 10 messages (memory)
        history = get_recent_messages(db, business_id=business_id, phone=phone, limit=10)

        # Generate reply with memory
        reply = generate_reply(Body, status=status, business_id=business_id, history=history)

        # Store assistant message
        add_message(db, business_id=business_id, phone=phone, role="assistant", content=reply)

        # Save lead snapshot
        upsert_lead(db, business_id=business_id, phone=phone, status=status, last_message=Body, last_reply=reply)
    finally:
        db.close()

    logger.info(f"[{business_id}] Reply: {reply}")

    twilio_response = f"""
<Response>
    <Message>{reply}</Message>
</Response>
"""
    return PlainTextResponse(content=twilio_response, media_type="application/xml")
