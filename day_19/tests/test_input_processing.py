import unittest
import sys
sys.path.insert(0, '..')

from preprocessor import InputPreprocessor
from parser import InputParser, IntentClassifier, EntityExtractor
from context_manager import ContextManager
from input_processor import InputHandler


class TestPreprocessor(unittest.TestCase):
    
    def setUp(self):
        self.preprocessor = InputPreprocessor()
    
    def test_normalize_whitespace(self):
        result = self.preprocessor.normalize_whitespace("hello   world  \n\n  test")
        self.assertEqual(result, "hello world test")
    
    def test_clean_text(self):
        result = self.preprocessor.clean_text("hello\x00world\x01test")
        self.assertNotIn("\x00", result)
        self.assertNotIn("\x01", result)
    
    def test_validate_empty(self):
        with self.assertRaises(ValueError):
            self.preprocessor.validate("")
    
    def test_validate_too_long(self):
        long_text = "a" * 10001
        with self.assertRaises(ValueError):
            self.preprocessor.validate(long_text)
    
    def test_preprocess_full(self):
        result = self.preprocessor.preprocess("  hello   world  ")
        self.assertEqual(result, "hello world")


class TestIntentClassifier(unittest.TestCase):
    
    def setUp(self):
        self.classifier = IntentClassifier()
    
    def test_query_intent(self):
        self.assertEqual(self.classifier.classify("What is the weather?"), "query")
    
    def test_command_intent(self):
        self.assertEqual(self.classifier.classify("Create a new file"), "command")
    
    def test_greeting_intent(self):
        self.assertEqual(self.classifier.classify("Hello there"), "greeting")
    
    def test_unknown_intent(self):
        self.assertEqual(self.classifier.classify("Random text"), "unknown")


class TestEntityExtractor(unittest.TestCase):
    
    def setUp(self):
        self.extractor = EntityExtractor()
    
    def test_extract_dates(self):
        entities = self.extractor.extract("Meeting on 2024-01-15")
        self.assertIn("dates", entities)
        self.assertIn("2024-01-15", entities["dates"])
    
    def test_extract_keywords(self):
        entities = self.extractor.extract("Project DataPipeline")
        self.assertIn("keywords", entities)
        self.assertIn("Project", entities["keywords"])
    
    def test_no_entities(self):
        entities = self.extractor.extract("simple text")
        self.assertEqual(entities, {})


class TestParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = InputParser()
    
    def test_parse_structure(self):
        result = self.parser.parse("What is the date 2024-01-15?")
        self.assertIn("intent", result)
        self.assertIn("entities", result)
        self.assertIn("text", result)
    
    def test_parse_with_error(self):
        result = self.parser.parse("test")
        self.assertIsNotNone(result)


class TestContextManager(unittest.TestCase):
    
    def setUp(self):
        self.manager = ContextManager()
    
    def test_store_and_retrieve(self):
        self.manager.store_message("user1", "Hello")
        messages = self.manager.get_recent_messages("user1")
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["message"], "Hello")
    
    def test_limit_messages(self):
        for i in range(10):
            self.manager.store_message("user2", f"Message {i}")
        messages = self.manager.get_recent_messages("user2", limit=3)
        self.assertEqual(len(messages), 3)
    
    def test_preferences(self):
        self.manager.set_preference("user3", "lang", "en")
        self.assertEqual(self.manager.get_preference("user3", "lang"), "en")
    
    def test_enrich(self):
        parsed = {"intent": "query", "entities": {}, "text": "test"}
        enriched = self.manager.enrich(parsed, "user4")
        self.assertIn("context", enriched)
        self.assertIn("recent_messages", enriched["context"])


class TestInputHandler(unittest.TestCase):
    
    def setUp(self):
        self.handler = InputHandler()
    
    def test_process_success(self):
        result = self.handler.process("Hello world", "user5")
        self.assertTrue(result["success"])
        self.assertIn("data", result)
    
    def test_process_empty_input(self):
        result = self.handler.process("", "user6")
        self.assertFalse(result["success"])
        self.assertEqual(result["error_type"], "validation")
    
    def test_process_stores_history(self):
        self.handler.process("Test message", "user7")
        messages = self.handler.context_manager.get_recent_messages("user7")
        self.assertEqual(len(messages), 1)


if __name__ == "__main__":
    unittest.main()
