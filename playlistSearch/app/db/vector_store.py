from app.core.config import settings
from qdrant_client.models import VectorParams, Distance, KeywordIndexParams, KeywordIndexType
from qdrant_client import AsyncQdrantClient


async def get_or_create_collection(qdrant_client: AsyncQdrantClient):
    """Checks if the Qdrant collection exists and creates it if it does not."""

    exists = await qdrant_client.collection_exists(settings.COLLECTION_NAME)

    if exists:
        print(f"Collection {settings.COLLECTION_NAME} already exists")
    else:
        await qdrant_client.create_collection(
            collection_name=settings.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=settings.EMBEDDING_SIZE,
                distance=Distance.COSINE
            )
        )
        print(f"Collection {settings.COLLECTION_NAME} created")

        await qdrant_client.create_payload_index(
            collection_name=settings.COLLECTION_NAME,
            field_name="user_id",  # The payload key you use to identify users
            field_schema=KeywordIndexParams(
                type=KeywordIndexType.KEYWORD,
                is_tenant=True,
            ),
        )

        print(f"Payload index for 'user_id' created in collection {settings.COLLECTION_NAME}")
