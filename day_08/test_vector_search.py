from vector_search import get_embedding
import chromadb

def test_embedding_generation():
    """Test that embeddings are generated correctly"""
    text = "test document"
    embedding = get_embedding(text)
    assert isinstance(embedding, list)
    assert len(embedding) == 1536  # text-embedding-3-small dimension

def test_search_functionality():
    """Test vector search returns relevant results"""
    # Create test collection
    test_client = chromadb.Client()
    test_collection = test_client.create_collection("test_docs")
    
    # Test documents
    docs = [
        "Python programming language",
        "JavaScript web development", 
        "Machine learning algorithms"
    ]
    
    embeddings = [get_embedding(doc) for doc in docs]
    ids = [f"test_{i}" for i in range(len(docs))]
    
    test_collection.add(
        embeddings=embeddings,
        documents=docs,
        ids=ids
    )
    
    # Search for programming-related content
    query_embedding = get_embedding("programming")
    results = test_collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )
    
    assert len(results["documents"][0]) == 2
    assert "Python" in results["documents"][0][0]

if __name__ == "__main__":
    test_embedding_generation()
    test_search_functionality()
    print("All tests passed!")