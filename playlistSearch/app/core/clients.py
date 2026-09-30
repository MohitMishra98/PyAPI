from qdrant_client import AsyncQdrantClient
from groq import Groq
from google import genai
from app.core.config import settings

qdrant_client = AsyncQdrantClient(
    api_key=settings.QDRANT_API_KEY,
    url=settings.QDRANT_URL
)

groq_client = Groq(api_key=settings.GROQ_API_KEY)

google_clinet = genai.Client(api_key=settings.GEMINI_API_KEY)