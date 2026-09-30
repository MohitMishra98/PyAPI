from fastapi import APIRouter, Depends, HTTPException, status
from qdrant_client import AsyncQdrantClient
from groq import AsyncGroq

from app.api.dependencies import get_current_user, get_qdrant_client, get_groq_client, get_google_client
from app.models.user import User
from app.schemas.msg import Msg

from app.rag.collect_data import get_transcriptions
from app.rag.rag_ingestion import ingest
from app.rag.search_text import get_sources_for_query

router = APIRouter()

@router.post("/")
async def create_source(
        playlist_url: str,
        current_user: User = Depends(get_current_user),
        qdrant_client: AsyncQdrantClient = Depends(get_qdrant_client),
        google_client = Depends(get_google_client)
    ):
    """
    Endpoint to create a new source based on the provided playlist URL.
    """
    try:
        data = get_transcriptions(playlist_url=playlist_url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch transcriptions: {str(e)}"
        )

    if not data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Youtube is blocking requests"
        )

    # ingest data into qdrant
    await ingest(
        data=data, 
        user_id=str(current_user.id),
        qdrant_client=qdrant_client,
        google_client=google_client
    )

    return Msg(message="Source created successfully")


@router.get("/")
async def get_sources(
        user_query: str,
        current_user: User = Depends(get_current_user),
        qdrant_client: AsyncQdrantClient = Depends(get_qdrant_client),
        groq_client: AsyncGroq = Depends(get_groq_client),
        google_client = Depends(get_google_client)
):
    sources = await get_sources_for_query(
        user_id=str(current_user.id), 
        user_query=user_query, 
        qdrant_client=qdrant_client,
        google_client=google_client,
        groq_client=groq_client,
    )

    return sources
