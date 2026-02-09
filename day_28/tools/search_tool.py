"""Search tool for text search operations."""

from typing import Dict, Any, List


def search(query: str, data: List[str] = None) -> Dict[str, Any]:
    """
    Search for text in a list of strings.
    
    Args:
        query: Search query string
        data: List of strings to search (uses mock data if None)
    
    Returns:
        Dict with search results and metadata
    """
    try:
        if not query:
            return {'success': False, 'error': 'Query cannot be empty'}
        
        # Mock data if none provided
        if data is None:
            data = [
                'Python is a programming language',
                'AI agents use tools to perform tasks',
                'Machine learning models need training data',
                'Natural language processing is a subfield of AI',
                'APIs enable communication between systems'
            ]
        
        query_lower = query.lower()
        matches = [item for item in data if query_lower in item.lower()]
        
        return {
            'success': True,
            'query': query,
            'matches': matches,
            'count': len(matches),
            'total_searched': len(data)
        }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}
