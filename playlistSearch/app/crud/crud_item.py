import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def get_multi_by_owner(
        self, db: Session, *, owner_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        """
        Fetch items belonging to a specific owner.
        """
        return (
            db.query(self.model)
            .filter(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_owner(
        self, db: Session, *, obj_in: ItemCreate, owner_id: uuid.UUID
    ) -> Item:
        """
        Create a new item associated with an owner.
        """
        db_obj = self.model(**obj_in.model_dump(), owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_owner_and_id(
        self, db: Session, *, id: uuid.UUID, owner_id: uuid.UUID
    ) -> Optional[Item]:
        """
        Fetch a specific item by id and owner_id.
        """
        return (
            db.query(self.model)
            .filter(Item.id == id, Item.owner_id == owner_id)
            .first()
        )


crud_item = CRUDItem(Item)
