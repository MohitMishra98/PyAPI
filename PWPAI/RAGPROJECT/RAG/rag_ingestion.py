from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os
import json

load_dotenv()

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
QDRANT_URL = os.getenv("QDRANT_URL", "")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "")
EMBEDDING_SIZE = int(os.getenv("EMBEDDING_SIZE",""))

qdrant_client = QdrantClient(
    api_key=QDRANT_API_KEY,
    url=QDRANT_URL
)

print("Connected to qdrant")

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

data = []

with open("data.json", "r") as file:
    data = json.load(file)

print("Data loaded")

# step1: setup the collection

# if collection already exists, delete it
if qdrant_client.collection_exists("knowledge"):
    print("Deleting collection knowledge")
    qdrant_client.delete_collection("knowledge")

# create new collection
qdrant_client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
            size=EMBEDDING_SIZE,
            distance=Distance.COSINE
    )
)

print("New collection created")

# step2: create embeddings
list_of_transcription_entries = data.get("transcription")

list_of_transcription_text = [text.get("text") for text in list_of_transcription_entries]

print(list_of_transcription_text)

text_embeddings = embedding_model.encode(list_of_transcription_text)
print("Embeddings created successfully")

# step3: now create points 

points = []

for i in range(len(list_of_transcription_text)):
    point = PointStruct(
        id=i+1,
        vector=text_embeddings[i].tolist(),
        payload=list_of_transcription_entries[i]
    )

    points.append(point)

# step4: upload points to qdrant
qdrant_client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print(f"Uploaded {len(text_embeddings)} to qdrant")

def ingest():
    pass