# Embedding Search Documentation

## Overview

The Embedding Search system provides semantic document search using OpenAI embeddings and cosine similarity. It allows you to find documents similar to a query based on meaning rather than exact keyword matches.

## Features

- **Semantic Search**: Uses OpenAI's text-embedding-3-small model for meaningful text representations
- **Cosine Similarity**: Calculates similarity between document vectors
- **Error Handling**: Gracefully handles API failures, empty inputs, and edge cases
- **Flexible Results**: Returns top-k most similar documents with similarity scores

## Installation

```bash
pip install openai numpy python-dotenv
```

## Setup

1. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

2. Import and use the EmbeddingSearch class:
```python
from embedding_search import EmbeddingSearch
```

## Usage

### Basic Usage

```python
# Initialize search engine
search = EmbeddingSearch()

# Add documents
documents = [
    "Python is a programming language",
    "Machine learning uses algorithms",
    "Cooking requires ingredients"
]
search.add_documents(documents)

# Search for similar documents
results = search.search("programming", top_k=2)

# Display results
for result in results:
    print(f"Similarity: {result['similarity']:.3f}")
    print(f"Document: {result['document']}")
```

### Advanced Usage

```python
# Search with different parameters
results = search.search("artificial intelligence", top_k=5)

# Handle empty results
if not results:
    print("No similar documents found")
```

## API Reference

### EmbeddingSearch Class

#### `__init__()`
Initialize an empty search engine.

#### `add_documents(texts: list)`
Add documents to the search index.

**Parameters:**
- `texts` (list): List of text documents to index

**Example:**
```python
search.add_documents([
    "Document 1 content",
    "Document 2 content"
])
```

#### `search(query: str, top_k: int = 3)`
Search for similar documents.

**Parameters:**
- `query` (str): Search query text
- `top_k` (int): Number of results to return (default: 3)

**Returns:**
- List of dictionaries with `document` and `similarity` keys

**Example:**
```python
results = search.search("machine learning", top_k=5)
```

### Utility Functions

#### `get_embedding(text: str)`
Generate embedding vector for text using OpenAI API.

**Parameters:**
- `text` (str): Input text

**Returns:**
- List of floats (embedding vector) or None if error

#### `cosine_similarity(vec1, vec2)`
Calculate cosine similarity between two vectors.

**Parameters:**
- `vec1`, `vec2`: Numpy arrays or lists

**Returns:**
- Float between -1 and 1 (similarity score)

## Error Handling

The system handles various error conditions:

- **API Failures**: Network issues, quota exceeded, invalid API keys
- **Empty Inputs**: Empty strings, None values, whitespace-only text
- **Mathematical Errors**: Zero vectors, division by zero
- **Missing Data**: No documents indexed, failed embeddings

All errors are logged with descriptive messages and the system continues operation where possible.

## Testing

Run the test suite:

```bash
python test_embedding_search.py
```

### Test Categories

1. **Functionality Tests**: Various queries with different document types
2. **Edge Case Tests**: Empty inputs, missing data, error conditions
3. **Mock Tests**: Fallback testing when API is unavailable

### Sample Test Queries

- Programming languages
- Artificial intelligence
- Food preparation
- Web development
- Database queries

## Performance Considerations

- **Embedding Generation**: Each document requires an API call (cached after creation)
- **Search Speed**: O(n) where n is number of documents
- **Memory Usage**: Stores all embeddings in memory
- **API Costs**: ~$0.00002 per 1K tokens for text-embedding-3-small

## Limitations

- Requires internet connection for OpenAI API
- Limited by OpenAI API rate limits and quotas
- All embeddings stored in memory (not persistent)
- No batch processing for large document sets

## Best Practices

1. **Batch Document Addition**: Add all documents at once when possible
2. **Error Handling**: Always check if results are empty
3. **API Key Security**: Use environment variables, never hardcode keys
4. **Text Preprocessing**: Clean and normalize text before embedding
5. **Result Validation**: Check similarity scores for relevance thresholds

## Example Applications

- **Document Search**: Find relevant documents in a knowledge base
- **Content Recommendation**: Suggest similar articles or products
- **FAQ Matching**: Match user questions to existing answers
- **Code Search**: Find similar code snippets or functions
- **Research**: Identify related academic papers or studies

## Troubleshooting

### Common Issues

1. **"No documents available for search"**
   - Solution: Add documents using `add_documents()` before searching

2. **"Error getting embedding: insufficient_quota"**
   - Solution: Check OpenAI account billing and usage limits

3. **Empty results**
   - Solution: Verify documents were added successfully, check API connectivity

4. **Low similarity scores**
   - Solution: Use more specific queries, add more relevant documents

### Debug Mode

Enable detailed error logging by checking the console output for specific error messages from each function.