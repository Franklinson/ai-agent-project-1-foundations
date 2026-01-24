import re
import unicodedata


class InputPreprocessor:
    """Preprocesses text input for AI agent processing."""
    
    def __init__(self, max_length=10000):
        self.max_length = max_length
    
    def normalize_whitespace(self, text):
        """Normalize whitespace to single spaces."""
        return re.sub(r'\s+', ' ', text).strip()
    
    def clean_text(self, text):
        """Remove control characters."""
        return ''.join(char for char in text if unicodedata.category(char)[0] != 'C' or char in '\n\t ')
    
    def validate(self, text):
        """Validate input text."""
        if not text or not text.strip():
            raise ValueError("Input cannot be empty")
        if len(text) > self.max_length:
            raise ValueError(f"Input exceeds maximum length of {self.max_length}")
        return True
    
    def normalize_encoding(self, text):
        """Normalize text encoding to NFC form."""
        return unicodedata.normalize('NFC', text)
    
    def preprocess(self, text):
        """Main preprocessing pipeline."""
        if not isinstance(text, str):
            text = str(text)
        
        self.validate(text)
        text = self.normalize_encoding(text)
        text = self.clean_text(text)
        text = self.normalize_whitespace(text)
        
        return text
