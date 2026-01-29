class ResultProcessor:
    def validate(self, result):
        """Validate result structure."""
        return isinstance(result, dict) and 'success' in result
    
    def extract_data(self, result):
        """Extract data from result."""
        if result.get('success'):
            return result.get('result')
        return result.get('error')
    
    def transform(self, data):
        """Transform data if needed."""
        return str(data) if data is not None else ''
    
    def process(self, result):
        """Process result through validation, extraction, and transformation."""
        if not self.validate(result):
            return {'valid': False, 'observation': 'Invalid result format'}
        
        data = self.extract_data(result)
        observation = self.transform(data)
        
        return {
            'valid': True,
            'success': result.get('success'),
            'observation': observation
        }
