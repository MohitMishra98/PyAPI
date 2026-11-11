from groq import Groq
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
llm_model = "openai/gpt-oss-120b"

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
QDRANT_URL = os.getenv("QDRANT_URL", "")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "")
EMBEDDING_SIZE = int(os.getenv("EMBEDDING_SIZE",""))

user_query = "what is word cloud"

qdrant_client = QdrantClient(
    api_key=QDRANT_API_KEY,
    url=QDRANT_URL
)

groq_client = Groq(api_key=GROQ_API_KEY)

def ask_llm(prompt, context):
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

def rewrite_user_query(original_query, language="English"):
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

def search(query, top_k):
    user_query_embedding = embedding_model.encode(query).tolist()

    # retrieve top k from qdrant
    result = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=user_query_embedding,
        limit=top_k,
        with_payload=True
    ).points

    return result

rewritten_user_query = rewrite_user_query(user_query) 

search_res = search(rewritten_user_query, 5)

print(search_res)

context = "".join([("DOCUMENT: " + result.payload["text"] + "\n\n") for result in search_res])

print(f"context: {context}")

llm_response = ask_llm(user_query, context)

print(llm_response)

json_response = {
    "userQuery": user_query,
    "modifiedUserQuery": rewritten_user_query,
    "modelResponse": llm_response,
    "sources": [result.payload for result in search_res]
}

print(json_response)