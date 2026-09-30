import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from qdrant_client import AsyncQdrantClient
from groq import Groq

from app.api.dependencies import get_current_user, get_db, get_qdrant_client, get_groq_client
from app.models.user import User
from app.schemas.msg import Msg

from app.rag.collect_data import get_transcriptions
from app.rag.rag_ingestion import ingest
from app.rag.search_text import get_sources_for_query

router = APIRouter()

router.post("/")
async def create_source(
        playlist_url: str,
        current_user: User = Depends(get_current_user),
        qdrant_client: AsyncQdrantClient = Depends(get_qdrant_client)
    ):
    """
    Endpoint to create a new source based on the provided playlist URL.
    """
    # get data  from playlist
    data = get_transcriptions(playlist_url=playlist_url)

    # ingest data into qdrant
    await ingest(
        data=data, 
        user_id=current_user.id,
        qdrant_client=qdrant_client
    )

    return Msg(message="Source created successfully")


router.get("/")
async def get_sources(
        user_query: str,
        current_user: User = Depends(get_current_user),
        qdrant_client: AsyncQdrantClient = Depends(get_qdrant_client),
        groq_client: Groq = Depends(get_groq_client)
):
    sources = await get_sources_for_query(
        user_id=current_user.id, 
        user_query=user_query, 
        qdrant_client=qdrant_client,
        groq_client=groq_client,
    )

    return sources
