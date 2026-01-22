CALCULATOR_TOOL_SCHEMA = {
    "name": "calculate",
    "description": "Perform basic mathematical operations: add, subtract, multiply, or divide two numbers",
    "parameters": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"],
                "description": "The mathematical operation to perform"
            },
            "a": {
                "type": "number",
                "description": "The first number"
            },
            "b": {
                "type": "number",
                "description": "The second number"
            }
        },
        "required": ["operation", "a", "b"]
    }
}

TEXT_TOOL_SCHEMA = [
    {
        "name": "word_count",
        "description": "Count the total number of words in a text string",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to analyze"
                }
            },
            "required": ["text"]
        }
    },
    {
        "name": "word_search",
        "description": "Count how many times a specific word appears in a text string (case-insensitive)",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to search in"
                },
                "word": {
                    "type": "string",
                    "description": "The word to search for"
                }
            },
            "required": ["text", "word"]
        }
    }
]

ALL_SCHEMAS = [CALCULATOR_TOOL_SCHEMA] + TEXT_TOOL_SCHEMA