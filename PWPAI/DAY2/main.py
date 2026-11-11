from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY","")

client = Groq(api_key=GROQ_API_KEY)

model = "openai/gpt-oss-120b"

usermessage = {
    "role": "user",
    "content": "who are you"
}

systemMessage = {
    "role": "system",
    "content": "you are an expert AI researcher"
}

messages = [usermessage, systemMessage]

response = client.chat.completions.create(
    model=model,
    messages=messages
)

output = response.choices[0].message.content

print("===="*50)
print(output)