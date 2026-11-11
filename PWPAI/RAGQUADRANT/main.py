from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
QDRANT_URL = os.getenv("QDRANT_URL", "")

groq_client = Groq(api_key=GROQ_API_KEY)

qdrant_client = QdrantClient(
    api_key=QDRANT_API_KEY,
    url=QDRANT_URL
)

print("Connected to Qdrant")

COLLECTION_NAME = "knowledge"
EMBEDDING_SIZE = 384

# delete collection if already exists
if qdrant_client.collection_exists(COLLECTION_NAME):
    print(f"Deleting collection {COLLECTION_NAME}")
    qdrant_client.delete_collection(COLLECTION_NAME)

# Create collection
qdrant_client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
            size=EMBEDDING_SIZE,
            distance=Distance.COSINE
    )
)

print(f"Collection created: {COLLECTION_NAME}")
print(f"Vector size: {EMBEDDING_SIZE}")
print(f"Distance: Cosine")


embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
llm_model = "openai/gpt-oss-120b"

documents = []

with open("knowledge.txt", "r", encoding="utf-8") as f:
    documents = [line.strip() for line in f if line.strip()]
    print(f"Documents loaded: {len(documents)}")

# create embeddings

embeddings = embedding_model.encode(documents)

print(f"Generated {len(embeddings)} embeddings")
print(f"Embedding size: {len(embeddings[0])}")

points = []

for i, embedding in enumerate(embeddings):
    point = PointStruct(
        id=i+1,
        vector=embedding.tolist(),
        payload={
            "text": documents[i]
        }
    )

    points.append(point)

# upload points to Qdrant
# upload + insert
qdrant_client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print(f"Uploaded {len(points)} points to qdrant")

def search(query, top_k):
    # convert query into embeddings
    query_embeddings = embedding_model.encode(query)

    # retrieve top k from qdrant
    result = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embeddings,
        limit=top_k,
        with_payload=True
    ).points

    return result

query = "how many vacation days do i get"

results = search(query, 3)

print("Query successful")
for result in results:
    print(f"ID:{result.id}")
    print(f"Score:{result.score}")
    print(f"Paylaod:{result.payload["text"]}")
    print()

def ask_llm(prompt, context):
    system_prompt = f"You are a helpful ai assistant you answer question only based on the context provided context: {context}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    response = groq_client.chat.completions.create(
        model=llm_model,
        messages=messages
    )

    return response.choices[0].message.content

context = "".join([result.payload["text"] for result in results])
print(f"context: {context}")

llm_response = ask_llm(query, context)

print(llm_response)