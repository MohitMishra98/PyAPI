from groq import AsyncGroq
from qdrant_client import AsyncQdrantClient
from app.core.config import settings
from qdrant_client.models import FieldCondition, MatchValue, Filter
from app.rag.generate_embeddings import embed_query
from google import genai

llm_model = settings.LLM_MODEL

async def ask_llm(prompt: str, context: str, groq_client: AsyncGroq):
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

    response = await groq_client.chat.completions.create(
        model=llm_model,
        messages=messages
    )

    return response.choices[0].message.content

async def rewrite_user_query(
        original_query: str, 
        groq_client: AsyncGroq, 
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

    response = await groq_client.chat.completions.create(
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
    query_result = await qdrant_client.query_points(
        collection_name=settings.COLLECTION_NAME,
        query=user_query_embedding,
        limit=top_k,
        query_filter=Filter(
            must=[
                # This ensures only vectors belonging to 'user_123' are searched
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=str(user_id))
                )
            ]
        ),
        with_payload=True
    )

    return query_result.points

async def get_sources_for_query(
        user_id: str, 
        user_query: str, 
        qdrant_client: AsyncQdrantClient,
        google_client: genai.Client,
        groq_client: AsyncGroq,
        top_k: int = 5,
    ):
    user_id_str = str(user_id)
    rewritten_user_query = await rewrite_user_query(
        original_query=user_query, 
        groq_client=groq_client
    ) 

    search_res = await search(
        user_id=user_id_str, 
        query=rewritten_user_query, 
        google_client=google_client,
        qdrant_client=qdrant_client,
        top_k=top_k
    )

    # if no sources were found no point of calling the llm
    if not search_res:
        json_response = {
                "user_id": user_id_str,
                "userQuery": user_query,
                "modifiedUserQuery": rewritten_user_query,
                "modelResponse": "",
                "sources": []
        }

        return json_response

    print(search_res)

    context = "".join([("DOCUMENT: " + str(result.payload.get("text", "")) + "\n\n") for result in search_res if result.payload])

    print(f"context: {context}")

    llm_response = await ask_llm(
        prompt=user_query, 
        context=context, 
        groq_client=groq_client
    )

    print(llm_response)

    sources = [
        {
            "videourl": result.payload.get("videourl", ""), 
            "videotitle": result.payload.get("videotitle", ""), 
            "timestamp": result.payload.get("timestamp", "")
        } 
        for result in search_res if result.payload and result.payload.get("text", "").strip()
    ]

    json_response = {
        "user_id": user_id_str,
        "userQuery": user_query,
        "modifiedUserQuery": rewritten_user_query,
        "modelResponse": llm_response,
        "sources": sources
    }

    print(json_response)

    return json_response