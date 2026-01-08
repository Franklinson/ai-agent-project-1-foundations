import chromadb
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("OpenAI API key loaded")
print('OPENAI_API_KEY' in os.environ)

# Initialize Chroma
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("documents")

def get_embedding(text):
    """Get embedding for text"""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Index documents
documents = [
    "Python is a programming language",
    "Machine learning uses algorithms",
    "Vector databases store embeddings"
]

embeddings = [get_embedding(doc) for doc in documents]
ids = [f"doc_{i}" for i in range(len(documents))]

collection.add(
    embeddings=embeddings,
    documents=documents,
    ids=ids
)

# Query
query_embedding = get_embedding("programming languages")
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

print("Search results:")
for doc, distance in zip(results["documents"][0], results["distances"][0]):
    print(f"Document: {doc}, Distance: {distance}")
