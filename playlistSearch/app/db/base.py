from sqlalchemy.orm import declarative_base

# Declarative base class for all SQLAlchemy ORM models
Base = declarative_base()

# Import all models here so that Base.metadata can discover them for migrations or create_all
from app.models.user import User  # noqa: F401, E402
from app.models.item import Item  # noqa: F401, E402
