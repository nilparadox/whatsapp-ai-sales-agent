from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging

from app.routes.root import router as root_router
from app.routes.health import router as health_router
from app.routes.whatsapp import router as whatsapp_router
from app.routes.leads import router as leads_router
from app.routes.send import router as send_router
from app.routes.admin import router as admin_router
from app.routes.dbinfo import router as dbinfo_router

from app.db.init_db import init_db
from app.core.seed import ensure_seed_files

logger = setup_logging()

app = FastAPI(title=settings.app_name)

app.include_router(root_router)
app.include_router(health_router)
app.include_router(whatsapp_router)
app.include_router(leads_router)
app.include_router(send_router)
app.include_router(admin_router)
app.include_router(dbinfo_router)

@app.on_event("startup")
def on_startup():
    ensure_seed_files()
    init_db()
    logger.info(f"Starting {settings.app_name} | env={settings.env}")
