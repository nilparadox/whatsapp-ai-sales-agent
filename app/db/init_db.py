from app.db.database import Base, engine

def init_db() -> None:
    # Ensure all models are imported so Base.metadata includes them
    import app.db.models  # noqa: F401
    Base.metadata.create_all(bind=engine)
