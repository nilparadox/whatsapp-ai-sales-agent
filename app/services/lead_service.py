from sqlalchemy.orm import Session
from datetime import datetime
from app.db.models import Lead

def upsert_lead(db: Session, business_id: str, phone: str, status: str, last_message: str, last_reply: str) -> Lead:
    lead = (
        db.query(Lead)
        .filter(Lead.business_id == business_id)
        .filter(Lead.phone == phone)
        .first()
    )
    now = datetime.utcnow()

    if lead:
        lead.status = status
        lead.last_message = last_message
        lead.last_reply = last_reply
        lead.updated_at = now
    else:
        lead = Lead(
            business_id=business_id,
            phone=phone,
            status=status,
            last_message=last_message,
            last_reply=last_reply,
            created_at=now,
            updated_at=now
        )
        db.add(lead)

    db.commit()
    db.refresh(lead)
    return lead
