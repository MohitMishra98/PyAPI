from fastapi import APIRouter, Depends, HTTPException, status
from qdrant_client import AsyncQdrantClient
from groq import AsyncGroq

from app.api.dependencies import get_current_user, get_qdrant_client, get_groq_client, get_google_client
from app.models.user import User

from app.services.rag_service import create_source, get_sources

router = APIRouter()

@router.post("/")
async def new_source(
        playlist_url: str,
        current_user: User = Depends(get_current_user),
        qdrant_client: AsyncQdrantClient = Depends(get_qdrant_client),
        google_client = Depends(get_google_client)
    ):
    """
    Endpoint to create a new source based on the provided playlist URL.
    """

    return await create_source(
        playlist_url=playlist_url,
        current_user=current_user,
        qdrant_client=qdrant_client,
        google_client=google_client
    )

@router.get("/")
async def get_existing_sources(
        user_query: str,
        current_user: User = Depends(get_current_user),
        qdrant_client: AsyncQdrantClient = Depends(get_qdrant_client),
        groq_client: AsyncGroq = Depends(get_groq_client),
        google_client = Depends(get_google_client)
):
    sources = await get_sources(
        user_id=str(current_user.id), 
        user_query=user_query, 
        qdrant_client=qdrant_client,
        google_client=google_client,
        groq_client=groq_client,
    )

    return sources
