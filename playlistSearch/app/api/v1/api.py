from fastapi import APIRouter

from app.api.v1.endpoints import users, playlist

api_router = APIRouter()

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)

api_router.include_router(
    playlist.router,
    prefix="/playlist",
    tags=["playlist"],
)
