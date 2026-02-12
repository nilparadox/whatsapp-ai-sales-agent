from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.db.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    business_id = Column(String(64), index=True, nullable=False, default="default")
    phone = Column(String(64), index=True, nullable=False)

    status = Column(String(32), nullable=False, default="NEW")  # NEW | INQUIRY | BOOKING

    last_message = Column(Text, nullable=False)
    last_reply = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    business_id = Column(String(64), index=True, nullable=False, default="default")
    phone = Column(String(64), index=True, nullable=False)

    role = Column(String(16), nullable=False)  # "user" | "assistant"
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
