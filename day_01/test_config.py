"""
Test script to verify environment variables are loaded correctly.
"""
import sys
from config import config

def test_config():
    """Test that configuration loads correctly."""
    print("Testing environment variable configuration...")
    print("-" * 50)
    
    # Test application settings
    print(f"App Name: {config.APP_NAME}")
    print(f"Debug Mode: {config.DEBUG}")
    print(f"Port: {config.PORT}")
    
    # Test API keys (should show None or placeholder warning)
    openai_key = config.get_openai_key()
    anthropic_key = config.get_anthropic_key()
    
    if openai_key:
        print(f"OpenAI API Key: {openai_key[:10]}... (loaded)")
    else:
        print("OpenAI API Key: Not set or using placeholder")
    
    if anthropic_key:
        print(f"Anthropic API Key: {anthropic_key[:10]}... (loaded)")
    else:
        print("Anthropic API Key: Not set or using placeholder")
    
    print("-" * 50)
    print("Configuration test complete!")
    
    # Validate configuration
    if config.validate():
        print("✓ Configuration is valid")
        return 0
    else:
        print("✗ Configuration validation failed")
        return 1

if __name__ == "__main__":
    sys.exit(test_config())