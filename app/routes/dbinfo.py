from fastapi import APIRouter
from app.db.database import DATABASE_URL

router = APIRouter()

@router.get("/dbinfo")
def dbinfo():
    # do NOT expose full credentials
    if DATABASE_URL.startswith("postgresql"):
        return {"db": "postgresql"}
    if DATABASE_URL.startswith("sqlite"):
        return {"db": "sqlite"}
    return {"db": "unknown"}
