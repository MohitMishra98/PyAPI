from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel
import os
from enum import Enum
import json


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY","")

client = Groq(api_key=GROQ_API_KEY)

model = "openai/gpt-oss-120b"


class IssueCategory(str, Enum):
    ELECTRONICS = "electronics"
    FOOD = "food"
    OTHER = "other"

class Ticket(BaseModel):
    name: str
    email: str
    issue_descrption: str
    issue_category: IssueCategory

schema = Ticket.model_json_schema()

print(schema)

response_format = {
    "type": "json_object"
}

system_prompt=f"Extract the personal information from the ticket strictly based on this schema and give a json output. {schema}"

system_message = {
    "role": "system",
    "content": system_prompt
}

text = "i bought a iphone form your store and it stopped working my name is pratyush and my email is pratyuhs@gmail.com"

user_prompt = f"please read the following user message and extract the key details \n\n {text}"

user_message = {
    "role": "user",
    "content": user_prompt
}

messages = [system_message, user_message]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format
)

# raw json string
output = response.choices[0].message.content

print(output)

# converts to python dict
intermedaite_json = json.loads(output)

print(intermedaite_json)

json_object = Ticket(**intermedaite_json)

print(json_object)