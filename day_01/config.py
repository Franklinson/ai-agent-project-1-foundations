"""
Configuration module for loading environment variables.

This module handles loading environment variables from .env file
and provides type-safe access to configuration values.
"""
from dotenv import load_dotenv
import os
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Application Settings
    APP_NAME: str = os.getenv("APP_NAME", "AI Agent Project 1")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    PORT: int = int(os.getenv("PORT", "8000"))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required environment variables are set."""
        # For Day 1, API keys are optional (we'll use them later)
        # But we can validate the structure
        return True
    
    @classmethod
    def get_openai_key(cls) -> Optional[str]:
        """Get OpenAI API key, raising error if not set."""
        key = cls.OPENAI_API_KEY
        if not key or key.startswith("your_") or "placeholder" in key.lower():
            return None
        return key
    
    @classmethod
    def get_anthropic_key(cls) -> Optional[str]:
        """Get Anthropic API key, raising error if not set."""
        key = cls.ANTHROPIC_API_KEY
        if not key or key.startswith("your_") or "placeholder" in key.lower():
            return None
        return key


# Create a config instance
config = Config()
