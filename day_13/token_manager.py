import tiktoken

class TokenManager:
    def __init__(self, model="gpt-4", budget=100000):
        self.model = model
        self.encoding = tiktoken.encoding_for_model(model)
        self.budget = budget
        self.used = 0
    
    def count_tokens(self, text):
        """Count tokens in text"""
        return len(self.encoding.encode(text))
    
    def can_add(self, text):
        """Check if text fits in budget"""
        tokens = self.count_tokens(text)
        return self.used + tokens <= self.budget
    
    def add(self, text):
        """Add text to budget"""
        tokens = self.count_tokens(text)
        if not self.can_add(text):
            raise ValueError(f"Exceeds budget: {tokens} tokens")
        self.used += tokens
        return tokens
    
    def remaining(self):
        """Get remaining tokens"""
        return self.budget - self.used

# Test
if __name__ == "__main__":
    manager = TokenManager(budget=1000)
    text = input("Enter text: ")
    tokens = manager.add(text)
    remaining = manager.remaining()
    
    output = f"Text: {text}\nTokens used: {tokens}\nRemaining: {remaining}\n"
    
    with open("token_output.txt", "w") as f:
        f.write(output)
    
    print("Output saved to token_output.txt")
