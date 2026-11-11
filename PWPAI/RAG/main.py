from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

client = Groq(api_key=GROQ_API_KEY)

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
llm_model = "openai/gpt-oss-120b"

documents = [
    "Employees receive 24 days of paid leave per year.",  
    "Employees work from the office on Tuesday, Wednesday and Thursday. "
    "Monday and Friday are optional work-from-home days.",
    "Employees receive Rs 3000 per month for gym reimbursement.",
    "Employees can claim Rs 2000 per month for home internet.",
    "Employees have a 90 day notice period."
]

def ask_llm(prompt, context):
    system_prompt = f"You are a helpful ai assistant you answer question only based on the context provided context: {context}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(
        model=llm_model,
        messages=messages
    )

    return response.choices[0].message.content

# array of embeddings for the documents
embeddings = embedding_model.encode(documents)

query = "how much vacations do i get"

query_embeddings = embedding_model.encode(query)

def retrieve(query_embeddings, topN, threshold):
    matches = [(cosine_similarity(query_embeddings, embeddings[i]), documents[i]) for i in range(len(documents))]

    matches = [i for i in matches if i[0] > threshold]
    # sort matches according to similarity
    matches.sort(reverse=True, key= lambda x: x[0])

    print(matches)

    return [i[1] for i in matches][:topN]

topN = 2

context = retrieve(query_embeddings, topN, 0.4)

print(context)

llm_response = ask_llm(query, context)

print(llm_response)