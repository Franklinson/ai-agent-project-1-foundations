class PromptLibrary:
    def __init__(self):
        self.prompts = {
            "summarize": "Summarize in {length} sentences: {text}",
            "classify": "Classify sentiment (positive/negative/neutral): {text}",
            "extract": "Extract {entity_type}: {text}",
            "translate": "Translate to {language}: {text}"
        }
    
    def get_prompt(self, name, **kwargs):
        return self.prompts[name].format(**kwargs)

# Example usage
library = PromptLibrary()

# Examples
print(library.get_prompt("summarize", text="AI is transforming industries", length=1))
print(library.get_prompt("classify", text="I love this product!"))
print(library.get_prompt("extract", text="John works at Google", entity_type="names"))

# Documentation
DOCS = """
Prompt Library Usage:
- summarize: Condense text to specified length
- classify: Determine sentiment polarity  
- extract: Pull specific entities from text
- translate: Convert text to target language
"""