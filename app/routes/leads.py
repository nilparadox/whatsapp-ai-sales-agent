from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Lead

router = APIRouter()

@router.get("/leads")
def list_leads(limit: int = 50, bid: str = Query(default="default")):
    business_id = (bid or "default").strip()
    db: Session = SessionLocal()
    try:
        leads = (
            db.query(Lead)
            .filter(Lead.business_id == business_id)
            .order_by(Lead.updated_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "id": l.id,
                "business_id": l.business_id,
                "phone": l.phone,
                "status": l.status,
                "last_message": l.last_message,
                "last_reply": l.last_reply,
                "created_at": l.created_at.isoformat(),
                "updated_at": l.updated_at.isoformat(),
            }
            for l in leads
        ]
    finally:
        db.close()
