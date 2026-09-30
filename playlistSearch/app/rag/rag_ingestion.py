from sentence_transformers import SentenceTransformer
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, KeywordIndexParams, KeywordIndexType
from app.core.config import settings
from google import genai
from app.rag.generate_embeddings import embed_documents

async def ingest(
        data: dict, 
        user_id: str, 
        qdrant_client: AsyncQdrantClient,
        google_client: genai.Client
    ):

    # create embeddings
    list_of_transcription_entries = data.get("transcription")

    list_of_transcription_text = [text.get("text") for text in list_of_transcription_entries]

    print(list_of_transcription_text)

    # Use the embedding model to create embeddings for the transcription text
    text_embeddings = await embed_documents(
        texts=list_of_transcription_text, 
        client=google_client
    )

    print("Embeddings created successfully")

    # now create points 

    points = []

    for i in range(len(list_of_transcription_text)):
        point = PointStruct(
            id=i+1,
            vector=text_embeddings[i].tolist(),
            payload={**list_of_transcription_entries[i], "user_id": user_id}
        )

        points.append(point)

    # upload points to qdrant
    await qdrant_client.upsert(
        collection_name=settings.COLLECTION_NAME,
        points=points
    )

    print(f"Uploaded {len(text_embeddings)} to qdrant")