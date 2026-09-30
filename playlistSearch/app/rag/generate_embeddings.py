from google import genai
from google.genai import types

async def embed_documents(texts: list[str], client: genai.Client) -> list[list[float]]:
    """Used when chunking and saving documents into Qdrant."""
    result = await client.models.embed_content(
        model="gemini-embedding-002",
        contents=texts,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=768
        )
    )
    return [embedding.values for embedding in result.embeddings]

async def embed_query(query: str, client: genai.Client) -> list[float]:
    """Used at runtime when the user asks a question."""
    result = await client.models.embed_content(
        model="gemini-embedding-002",
        contents=query,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=768
        )
    )
    return result.embeddings[0].values