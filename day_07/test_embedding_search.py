import os
from dotenv import load_dotenv
from embedding_search import EmbeddingSearch
import numpy as np

load_dotenv()

def test_embedding_search():
    """Test embedding search with various queries"""
    
    # Sample documents
    documents = [
        "Python is a high-level programming language",
        "Machine learning algorithms analyze data patterns",
        "Cooking pasta requires boiling water and salt",
        "JavaScript runs in web browsers",
        "Deep learning uses neural networks",
        "Baking bread needs flour, water, and yeast",
        "SQL queries databases for information",
        "Natural language processing understands text",
        "Pizza is made with dough, sauce, and cheese",
        "React is a JavaScript library for UI"
    ]
    
    # Test queries
    test_queries = [
        "programming languages",
        "artificial intelligence",
        "food preparation",
        "web development",
        "database queries",
        "cooking recipes",
        "software engineering",
        "machine learning models"
    ]
    
    print("Embedding Search Test Results")
    print("=" * 50)
    
    # Initialize search
    search = EmbeddingSearch()
    search.add_documents(documents)
    
    if not search.documents:
        print("API unavailable - running mock test")
        run_mock_test()
        return
    
    # Test each query
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 30)
        
        results = search.search(query, top_k=3)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"{i}. Similarity: {result['similarity']:.3f}")
                print(f"   Document: {result['document']}")
        else:
            print("No results found")
        print()

def run_mock_test():
    """Run test with mock embeddings when API unavailable"""
    np.random.seed(42)
    
    documents = [
        "Python programming language",
        "Machine learning algorithms", 
        "Cooking pasta recipe"
    ]
    
    queries = ["programming", "AI", "food"]
    
    for query in queries:
        print(f"\nMock Query: '{query}'")
        print("-" * 20)
        
        # Mock similarity scores
        scores = np.random.rand(len(documents))
        sorted_indices = np.argsort(scores)[::-1]
        
        for i, idx in enumerate(sorted_indices):
            print(f"{i+1}. Similarity: {scores[idx]:.3f}")
            print(f"   Document: {documents[idx]}")

def test_edge_cases():
    """Test edge cases and error handling"""
    print("\nEdge Case Tests")
    print("=" * 30)
    
    search = EmbeddingSearch()
    
    # Test empty query
    print("1. Empty query test:")
    results = search.search("")
    print(f"Results: {len(results)} documents found\n")
    
    # Test search without documents
    print("2. No documents test:")
    results = search.search("test query")
    print(f"Results: {len(results)} documents found\n")
    
    # Test with empty document list
    print("3. Empty document list test:")
    search.add_documents([])
    results = search.search("test")
    print(f"Results: {len(results)} documents found\n")

if __name__ == "__main__":
    test_embedding_search()
    test_edge_cases()