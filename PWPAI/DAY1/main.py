from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

client  = Groq(api_key=GROQ_API_KEY)

print(client)

model = "openai/gpt-oss-120b"

message = {
    "role": "user",
    "content": "How are you"
}

messages = [message]

response = client.chat.completions.create(
    model=model,
    messages=messages
)

content = response.choices[0].message.content

print(response)

print("="*50)

print(content)