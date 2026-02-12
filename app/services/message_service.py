from typing import List, Dict
from sqlalchemy.orm import Session
from app.db.models import Message

def add_message(db: Session, business_id: str, phone: str, role: str, content: str) -> None:
    m = Message(business_id=business_id, phone=phone, role=role, content=content)
    db.add(m)
    db.commit()

def get_recent_messages(db: Session, business_id: str, phone: str, limit: int = 10) -> List[Dict[str, str]]:
    rows = (
        db.query(Message)
        .filter(Message.business_id == business_id)
        .filter(Message.phone == phone)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )
    rows = list(reversed(rows))
    return [{"role": r.role, "content": r.content} for r in rows]
