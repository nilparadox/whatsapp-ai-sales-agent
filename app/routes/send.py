from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.twilio_service import send_whatsapp

router = APIRouter()

class SendRequest(BaseModel):
    to: str
    message: str

@router.post("/send")
def send(req: SendRequest):
    try:
        sid = send_whatsapp(req.to, req.message)
        return {"status": "sent", "sid": sid}
    except Exception as e:
        # Return JSON, not plain text 500
        raise HTTPException(status_code=400, detail=str(e))
