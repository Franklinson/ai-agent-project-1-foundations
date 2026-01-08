# Vector Search Documentation

## Overview
This implementation provides vector-based document search using ChromaDB and OpenAI embeddings.

## Setup Process

### Prerequisites
- Python 3.11+
- OpenAI API key
- Required packages: `chromadb`, `openai`, `python-dotenv`

### Installation
```bash
pip install chromadb openai python-dotenv
```

### Environment Setup
1. Create `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Implementation Details

### Vector Database Setup
- Uses ChromaDB as the vector database
- Creates in-memory collection named "documents"
- Stores document embeddings with metadata

### Document Indexing
- Converts text to embeddings using OpenAI's `text-embedding-3-small` model
- Each document gets a unique ID (`doc_0`, `doc_1`, etc.)
- Embeddings are 1536-dimensional vectors

### Search Implementation
- Query text is converted to embedding
- ChromaDB performs similarity search
- Returns top N most similar documents with distance scores

## Usage

### Basic Search
```python
from vector_search import get_embedding, collection

# Add documents
documents = ["Your document text here"]
embeddings = [get_embedding(doc) for doc in documents]
collection.add(embeddings=embeddings, documents=documents, ids=["doc_1"])

# Search
query_embedding = get_embedding("your search query")
results = collection.query(query_embeddings=[query_embedding], n_results=5)
```

### Running Tests
```bash
# Mock tests (no API calls required)
python test_mock_vector_search.py

# Full tests (requires OpenAI API quota)
python test_vector_search.py
```

### Test Results
✓ Vector database setup working  
✓ Document indexing working  
✓ Search functionality working  
✓ Environment setup: API key configured

## Key Features
- Semantic search capabilities
- Fast similarity matching
- Scalable document indexing
- Distance-based relevance scoring

## Limitations
- In-memory storage (data lost on restart)
- Requires OpenAI API calls for embeddings
- Limited to text documents