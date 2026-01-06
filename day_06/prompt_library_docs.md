# Prompt Library Documentation

## Overview
Simple prompt template library for common NLP tasks.

## Usage
```python
from prompt_library import PromptLibrary
library = PromptLibrary()
```

## Available Prompts

### summarize
Condense text to specified length.
```python
library.get_prompt("summarize", text="Long text", length=2)
```

### classify  
Determine sentiment polarity.
```python
library.get_prompt("classify", text="I love this!")
```

### extract
Pull specific entities from text.
```python
library.get_prompt("extract", text="John at Google", entity_type="names")
```

### translate
Convert text to target language.
```python
library.get_prompt("translate", text="Hello", language="French")
```

## Examples
```python
# Summarization
prompt = library.get_prompt("summarize", 
    text="AI is transforming industries", length=1)

# Classification
prompt = library.get_prompt("classify", text="Amazing product!")

# Extraction  
prompt = library.get_prompt("extract",
    text="Apple CEO Tim Cook", entity_type="companies")
```