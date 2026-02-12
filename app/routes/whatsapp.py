from fastapi import APIRouter, Form, Query, HTTPException
from fastapi.responses import PlainTextResponse
from loguru import logger

from app.core.utils import normalize_whatsapp_from, detect_status
from app.services.ai_service import generate_reply
from app.services.lead_service import upsert_lead
from app.services.key_service import get_key
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

    reply = generate_reply(Body, status=status, business_id=business_id)
    logger.info(f"[{business_id}] Reply: {reply}")

    db = SessionLocal()
    try:
        upsert_lead(db, business_id=business_id, phone=phone, status=status, last_message=Body, last_reply=reply)
    finally:
        db.close()

    twilio_response = f"""
<Response>
    <Message>{reply}</Message>
</Response>
"""
    return PlainTextResponse(content=twilio_response, media_type="application/xml")
