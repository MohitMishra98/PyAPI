import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    owner = relationship("User", back_populates="items")

    def __repr__(self) -> str:
        return f"<Item id={self.id} title='{self.title}' owner_id={self.owner_id}>"
