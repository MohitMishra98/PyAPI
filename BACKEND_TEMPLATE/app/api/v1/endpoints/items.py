from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.crud.crud_item import crud_item
from app.crud.crud_user import crud_user
from app.models.item import Item
from app.models.user import User
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.schemas.msg import Msg

router = APIRouter()


@router.get(
    "/",
    response_model=List[ItemResponse],
    summary="Retrieve user's items",
)
def read_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve items belonging to the authenticated user.
    Superusers can view all items.
    """
    if crud_user.is_superuser(current_user):
        return crud_item.get_multi(db, skip=skip, limit=limit)
    return crud_item.get_multi_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit
    )


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an item",
)
def create_item(
    *,
    db: Session = Depends(get_db),
    item_in: ItemCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create a new item owned by the currently authenticated user.
    """
    item = crud_item.create_with_owner(
        db, obj_in=item_in, owner_id=current_user.id
    )
    return item


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get item by ID",
)
def read_item_by_id(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get a specific item by ID. Must be the owner or a superuser.
    """
    item = crud_item.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )
    if item.owner_id != current_user.id and not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this item.",
        )
    return item


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Update item by ID",
)
def update_item(
    item_id: int,
    *,
    db: Session = Depends(get_db),
    item_in: ItemUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update an item. Must be the owner or a superuser.
    """
    item = crud_item.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )
    if item.owner_id != current_user.id and not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify this item.",
        )
    return crud_item.update(db, db_obj=item, obj_in=item_in)


@router.delete(
    "/{item_id}",
    response_model=Msg,
    summary="Delete item by ID",
)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Delete an item. Must be the owner or a superuser.
    """
    item = crud_item.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )
    if item.owner_id != current_user.id and not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this item.",
        )
    crud_item.remove(db, id=item_id)
    return Msg(message="Item deleted successfully.")
