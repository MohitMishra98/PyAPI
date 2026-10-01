from fastapi import APIRouter, Depends, HTTPException, status
from qdrant_client import AsyncQdrantClient
from groq import AsyncGroq

from app.api.dependencies import get_current_user, get_qdrant_client, get_groq_client, get_google_client
from app.models.user import User
from app.schemas.msg import Msg

from app.rag.collect_data import get_transcriptions
from app.rag.rag_ingestion import ingest
from app.rag.search_text import get_sources_for_query
from app.rag.remove_points import remove_points_by_user_id
from google import genai


async def create_source(
        playlist_url: str,
        current_user: User,
        qdrant_client: AsyncQdrantClient,
        google_client 
    ):
    """
    service to create a new source based on the provided playlist URL.
    """

    # delete previous data sources for the user
    try:
        await remove_points_by_user_id(
            user_id=str(current_user.id),
            qdrant_client=qdrant_client
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove previous sources"
        )

    try:
        data = get_transcriptions(playlist_url=playlist_url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch transcriptions: {str(e)}"
        )

    if not data["transcription"]:
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


async def get_sources(
        user_id: str, 
        user_query: str, 
        qdrant_client: AsyncQdrantClient,
        google_client: genai.Client,
        groq_client: AsyncGroq,
        top_k: int = 5,
    ):

    try: 
        sources = await get_sources_for_query(
            user_id=user_id, 
            user_query=user_query, 
            qdrant_client=qdrant_client,
            google_client=google_client,
            groq_client=groq_client,
            top_k=top_k
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get sources: {str(e)}"
        )

    if not sources["sources"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You have no sources for this query. Please create a source first."
        )

    return sources