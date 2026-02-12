from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging

from app.routes.health import router as health_router
from app.routes.whatsapp import router as whatsapp_router
from app.routes.leads import router as leads_router
from app.routes.send import router as send_router
from app.routes.admin import router as admin_router

from app.db.init_db import init_db

logger = setup_logging()

app = FastAPI(title=settings.app_name)

app.include_router(health_router)
app.include_router(whatsapp_router)
app.include_router(leads_router)
app.include_router(send_router)
app.include_router(admin_router)

@app.on_event("startup")
def on_startup():
    init_db()
    logger.info(f"Starting {settings.app_name} | env={settings.env}")
