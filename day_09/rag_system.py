from openai import OpenAI
import chromadb
import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class RAGSystem:
    def __init__(self, collection_name: str = "knowledge"):
        """Initialize RAG system with OpenAI and ChromaDB"""
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.client = chromadb.Client()
        try:
            self.vector_db = self.client.get_collection(collection_name)
        except:
            self.vector_db = self.client.create_collection(collection_name)
    
    def setup_knowledge_base(self, documents: List[str], metadata: List[Dict] = None) -> None:
        """Set up knowledge base with documents"""
        if not documents:
            return
        
        embeddings = [self._get_embedding(doc) for doc in documents]
        ids = [f"doc_{i}" for i in range(len(documents))]
        
        self.vector_db.add(
            embeddings=embeddings,
            documents=documents,
            ids=ids
        )
    
    def retrieve_context(self, query: str, n_results: int = 3) -> List[str]:
        """Retrieve relevant context for query"""
        query_embedding = self._get_embedding(query)
        results = self.vector_db.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results["documents"][0] if results["documents"] else []
    
    def augment_prompt(self, query: str, context: List[str]) -> str:
        """Augment prompt with retrieved context"""
        context_text = "\n\n".join(context)
        return f"""Use the following context to answer the question. If the context doesn't contain relevant information, say so.

Context:
{context_text}

Question: {query}
Answer:"""
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using LLM"""
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    
    def query(self, question: str, n_results: int = 3) -> Dict[str, Any]:
        """Complete RAG pipeline: retrieve, augment, generate"""
        # Retrieve relevant context
        context = self.retrieve_context(question, n_results)
        
        # Augment prompt with context
        augmented_prompt = self.augment_prompt(question, context)
        
        # Generate response
        response = self.generate_response(augmented_prompt)
        
        return {
            "question": question,
            "context": context,
            "response": response,
            "context_count": len(context)
        }
    
    def _get_embedding(self, text: str) -> List[float]:
        """Get text embedding from OpenAI"""
        response = self.llm.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

def test_rag_system():
    """Test RAG system with various questions"""
    print("=== RAG System Test ===")
    
    # Initialize system
    rag = RAGSystem()
    
    # Knowledge base documents
    documents = [
        "Python is a high-level programming language known for its simplicity and readability.",
        "Machine learning is a subset of AI that uses algorithms to learn patterns from data.",
        "RAG (Retrieval-Augmented Generation) combines information retrieval with text generation.",
        "Vector databases store high-dimensional vectors for similarity search.",
        "OpenAI provides APIs for language models and embeddings.",
        "ChromaDB is an open-source vector database for AI applications.",
        "Natural Language Processing (NLP) helps computers understand human language.",
        "Deep learning uses neural networks with multiple layers to process data."
    ]
    
    # Set up knowledge base
    print("Setting up knowledge base...")
    rag.setup_knowledge_base(documents)
    print(f"Indexed {len(documents)} documents\n")
    
    # Test questions
    test_questions = [
        "What is RAG?",
        "How does machine learning work?",
        "What programming language is mentioned?",
        "Tell me about vector databases",
        "What is deep learning?",
        "How do I cook pasta?"  # Question not in knowledge base
    ]
    
    results = []
    
    for question in test_questions:
        print(f"Question: {question}")
        result = rag.query(question)
        print(f"Context found: {result['context_count']} documents")
        print(f"Answer: {result['response']}")
        print("-" * 50)
        
        results.append(result)
    
    return results

def save_test_results(results: List[Dict], filename: str = "rag_test_results.json"):
    """Save test results to file"""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Test results saved to {filename}")

if __name__ == "__main__":
    # Run tests
    test_results = test_rag_system()
    
    # Save results
    save_test_results(test_results)
