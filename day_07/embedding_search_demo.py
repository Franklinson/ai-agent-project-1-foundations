import os
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
from numpy.linalg import norm

load_dotenv()
client = OpenAI()

def get_embedding(text):
    """Get embedding for text"""
    try:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text.strip()
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return None

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity"""
    try:
        if vec1 is None or vec2 is None:
            return 0.0
        norm1, norm2 = norm(vec1), norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return np.dot(vec1, vec2) / (norm1 * norm2)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0

class EmbeddingSearch:
    def __init__(self):
        self.documents = []
        self.embeddings = []
    
    def add_documents(self, texts):
        """Add documents and create embeddings"""
        try:
            for text in texts:
                embedding = get_embedding(text)
                if embedding is not None:
                    self.documents.append(text)
                    self.embeddings.append(embedding)
        except Exception as e:
            print(f"Error adding documents: {e}")
    
    def search(self, query, top_k=3):
        """Search for similar documents"""
        try:
            if not self.documents:
                print("No documents available for search")
                return []
            
            query_embedding = get_embedding(query)
            if query_embedding is None:
                return []
            
            similarities = [
                cosine_similarity(query_embedding, emb)
                for emb in self.embeddings
            ]
            
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            return [
                {
                    "document": self.documents[i],
                    "similarity": similarities[i]
                }
                for i in top_indices
            ]
        except Exception as e:
            print(f"Error during search: {e}")
            return []

# Demo with mock embeddings (for testing without API calls)
def demo_with_mock_data():
    """Demo using mock embeddings to show functionality"""
    print("Demo: Embedding Search with Mock Data")
    print("=" * 40)
    
    # Mock embeddings (random vectors for demo)
    np.random.seed(42)
    mock_embeddings = {
        "Python is a programming language": np.random.rand(100),
        "Machine learning uses algorithms": np.random.rand(100),
        "Cooking requires ingredients": np.random.rand(100)
    }
    
    # Create search instance and manually add mock data
    search = EmbeddingSearch()
    for doc, emb in mock_embeddings.items():
        search.documents.append(doc)
        search.embeddings.append(emb)
    
    # Mock query embedding
    query_emb = np.random.rand(100)
    
    # Calculate similarities manually
    similarities = [cosine_similarity(query_emb, emb) for emb in search.embeddings]
    top_indices = np.argsort(similarities)[-3:][::-1]
    
    print("Query: 'programming'")
    print("Results:")
    for i in top_indices:
        print(f"Similarity: {similarities[i]:.3f}")
        print(f"Document: {search.documents[i]}\n")

if __name__ == "__main__":
    # Try real API first, fall back to demo
    print("Testing Embedding Search Implementation")
    print("=" * 40)
    
    search = EmbeddingSearch()
    search.add_documents([
        "Python is a programming language",
        "Machine learning uses algorithms", 
        "Cooking requires ingredients"
    ])
    
    if search.documents:
        results = search.search("programming")
        for result in results:
            print(f"Similarity: {result['similarity']:.3f}")
            print(f"Document: {result['document']}\n")
    else:
        print("API unavailable, running demo with mock data...\n")
        demo_with_mock_data()