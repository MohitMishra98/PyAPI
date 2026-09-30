from groq import Groq
from qdrant_client import AsyncQdrantClient
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from qdrant_client.models import FieldCondition, MatchValue, Filter
from app.rag.generate_embeddings import embed_query
from google import genai

llm_model = settings.LLM_MODEL

async def ask_llm(prompt: str, context: str, groq_client: Groq):
    system_prompt = f"""
    You are a helpful assistant you give meaningful answers to the user queries based on the context
    please do not provide answer if required information is not available in the context

    CONTEXT: {context}
    """

    system_message = {
        "role": "system",
        "content": system_prompt
    }

    user_message = {
        "role": "user",
        "content": prompt
    }

    messages = [system_message, user_message]

    response = groq_client.chat.completions.create(
        model=llm_model,
        messages=messages
    )

    return response.choices[0].message.content

async def rewrite_user_query(
        original_query: str, 
        groq_client: Groq, 
        language: str = "English"
    ):

    system_prompt = f"""
    You are a helpful assistant you rewrite the user query based on the context
    you only give me a single rewritten query based on the context, do not provide any other information and do not answer the query, only rewrite the query
    please privide the query re written in {language} language
    """

    system_message = {
        "role": "system",
        "content": system_prompt
    }

    user_message = {
        "role": "user",
        "content": original_query
    }

    messages = [system_message, user_message]

    response = groq_client.chat.completions.create(
        model=llm_model,
        messages=messages
    )

    return response.choices[0].message.content

async def search(
        user_id: str, 
        query: str, 
        qdrant_client: AsyncQdrantClient, 
        google_client: genai.Client,
        top_k: int = 5
    ):
    user_query_embedding = await embed_query(query=query, client=google_client)

    # retrieve top k from qdrant
    result = qdrant_client.query_points(
        collection_name=settings.COLLECTION_NAME,
        query=user_query_embedding,
        limit=top_k,
        query_filter=Filter(
            must=[
                # This ensures only vectors belonging to 'user_123' are searched
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user_id)
                )
            ]
        ),
        with_payload=True
    ).points

    return result

async def get_sources_for_query(
        user_id: str, 
        user_query: str, 
        qdrant_client: AsyncQdrantClient,
        google_client: genai.Client,
        groq_client: Groq,
        top_k: int = 5,
    ):
    rewritten_user_query = await rewrite_user_query(
        original_query=user_query, 
        groq_client=groq_client
    ) 

    search_res = await search(
        user_id=user_id, 
        query=rewritten_user_query, 
        google_client=google_client,
        qdrant_client=qdrant_client,
        top_k=top_k
    )

    print(search_res)

    context = "".join([("DOCUMENT: " + result.payload["text"] + "\n\n") for result in search_res])

    print(f"context: {context}")

    llm_response = await ask_llm(
        prompt=user_query, 
        context=context, 
        groq_client=groq_client
    )

    print(llm_response)

    json_response = {
        "user_id": user_id,
        "userQuery": user_query,
        "modifiedUserQuery": rewritten_user_query,
        "modelResponse": llm_response,
        "sources": [
            {
                "videourl": result.payload["videourl"], 
                "videotitle": result.payload["videotitle"], 
                "timestamp": result.payload["timestamp"]
            } 
            for result in search_res if result.payload["text"].strip()
        ]
    }

    print(json_response)

    return json_response