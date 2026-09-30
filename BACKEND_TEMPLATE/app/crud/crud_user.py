from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        Fetch a user by email address.
        """
        return db.query(User).filter(User.email == email.lower()).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Create a new user with bcrypt-hashed password and normalized lowercase email.
        """
        db_obj = User(
            email=obj_in.email.lower(),
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_active=True,
            is_verified=False,
            is_superuser=False,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]],
    ) -> User:
        """
        Update user profile, hashing new password if provided.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            db_obj.hashed_password = hashed_password

        if "email" in update_data and update_data["email"]:
            update_data["email"] = update_data["email"].lower()

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[User]:
        """
        Authenticate user by email and password.
        """
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def mark_as_verified(self, db: Session, *, user: User) -> User:
        """
        Mark a user's email address as verified.
        """
        user.is_verified = True
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update_password(self, db: Session, *, user: User, new_password: str) -> User:
        """
        Update a user's password directly.
        """
        user.hashed_password = get_password_hash(new_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_verified(self, user: User) -> bool:
        return user.is_verified

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


crud_user = CRUDUser(User)
