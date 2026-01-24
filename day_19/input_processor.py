from preprocessor import InputPreprocessor
from parser import InputParser
from context_manager import ContextManager


class InputHandler:
    """Main input processor integrating all components."""
    
    def __init__(self, max_length=10000):
        self.preprocessor = InputPreprocessor(max_length)
        self.parser = InputParser()
        self.context_manager = ContextManager()
    
    def process(self, raw_input, user_id):
        """Process input through full pipeline."""
        try:
            # Preprocess
            cleaned_text = self.preprocessor.preprocess(raw_input)
            
            # Parse
            parsed = self.parser.parse(cleaned_text)
            
            # Enrich with context
            enriched = self.context_manager.enrich(parsed, user_id)
            
            # Store in history
            self.context_manager.store_message(user_id, {
                'input': raw_input,
                'processed': cleaned_text,
                'intent': parsed['intent']
            })
            
            return {
                'success': True,
                'data': enriched
            }
            
        except ValueError as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': 'validation'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': 'processing'
            }
