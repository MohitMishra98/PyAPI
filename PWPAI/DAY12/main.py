from sentence_transformers import SentenceTransformer
import numpy as np

text1 = "There are 24 paid leaves"
text2 = "cat is a wild animal"

def cosine_simlarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# this model creates a 384 dimensional vector for each sentence
model = SentenceTransformer('all-MiniLM-L6-v2')

# embedding will be a numpy array of length 384 (dimensions)
embedding1 = model.encode(text1)
embedding2 = model.encode(text2)

print(f"Embedding for text1: {embedding1}")
print(f"Embedding for text2: {embedding2}")

similarity = cosine_simlarity(embedding1, embedding2)

print(f"Similarity :{similarity}")