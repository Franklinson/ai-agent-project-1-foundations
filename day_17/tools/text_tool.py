class TextTool:
    """Tool for performing text analysis operations."""
    
    def word_count(self, text: str) -> dict:
        """
        Count the number of words in text.
        
        Args:
            text: Input text string
            
        Returns:
            Dictionary with word count result
        """
        if not isinstance(text, str):
            return {"success": False, "error": "Input must be a string"}
        
        count = len(text.split())
        return {"success": True, "operation": "word_count", "count": count}
    
    def word_search(self, text: str, word: str) -> dict:
        """
        Count occurrences of a word in text.
        
        Args:
            text: Input text string
            word: Word to search for
            
        Returns:
            Dictionary with occurrence count
        """
        if not isinstance(text, str) or not isinstance(word, str):
            return {"success": False, "error": "Inputs must be strings"}
        
        if not word:
            return {"success": False, "error": "Search word cannot be empty"}
        
        count = text.lower().split().count(word.lower())
        return {"success": True, "operation": "word_search", "word": word, "count": count}