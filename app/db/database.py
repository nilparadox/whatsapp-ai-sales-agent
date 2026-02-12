import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------
# DATABASE URL RESOLUTION
# -------------------------------------------------
# Priority:
# 1. DATABASE_URL (Render Postgres)
# 2. Local SQLite fallback
# -------------------------------------------------

def get_database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()

    if url:
        # Render may give postgres:// but SQLAlchemy needs postgresql://
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

    # Local development fallback
    return "sqlite:///./app.db"


DATABASE_URL = get_database_url()

# SQLite needs special flag
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
