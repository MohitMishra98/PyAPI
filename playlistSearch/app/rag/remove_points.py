from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from app.core.config import settings

async def remove_points_by_user_id(
        user_id: str,
        qdrant_client: AsyncQdrantClient,
):
    # Delete points using a filter selector
    await qdrant_client.delete(
        collection_name=settings.COLLECTION_NAME,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="user_id", # The payload key to check
                        match=models.MatchValue(value=user_id),
                    ),
                ],
            )
        ),
    )