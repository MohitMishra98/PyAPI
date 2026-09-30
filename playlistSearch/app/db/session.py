from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# Engine configuration depending on DB type
connect_args = {}
engine_kwargs = {}

if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    # Production-ready PostgreSQL pooling settings
    engine_kwargs.update(
        {
            "pool_pre_ping": True,
            "pool_recycle": 300,
            "pool_size": 10,
            "max_overflow": 20,
        }
    )

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    **engine_kwargs,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides an independent database session for each request.
    Automatically closes the session once request execution completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
