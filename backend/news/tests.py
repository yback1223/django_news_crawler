from django.test import TestCase
from .gemini_work import GeminiWork

class CleanResponseTextTest(TestCase):
    def setUp(self):
        self.gemini_work = GeminiWork()

    def test_clean_response_text_basic(self):
        
        raw_text = 'This is a "test" string.'
        expected_cleaned_text = 'This is a \\"test\\" string.'
        cleaned_text = self.gemini_work.clean_response_text(raw_text)
        self.assertEqual(cleaned_text, expected_cleaned_text)

    def test_clean_response_text_no_quotes(self):
        
        raw_text = 'This is a test string without quotes.'
        expected_cleaned_text = raw_text  
        cleaned_text = self.gemini_work.clean_response_text(raw_text)
        self.assertEqual(cleaned_text, expected_cleaned_text)

    def test_clean_response_text_escaped_quotes(self):
        
        raw_text = 'This is a \\"test\\" string.'
        expected_cleaned_text = raw_text  
        cleaned_text = self.gemini_work.clean_response_text(raw_text)
        self.assertEqual(cleaned_text, expected_cleaned_text)

    def test_clean_response_text_mixed_quotes(self):
        
        raw_text = 'This is a "test\\" string.'
        expected_cleaned_text = 'This is a \\"test\\" string.'
        cleaned_text = self.gemini_work.clean_response_text(raw_text)
        self.assertEqual(cleaned_text, expected_cleaned_text)

    def test_clean_response_text_multiple_quotes(self):
        
        raw_text = '"First" and "Second" quotes.'
        expected_cleaned_text = '\\"First\\" and \\"Second\\" quotes.'
        cleaned_text = self.gemini_work.clean_response_text(raw_text)
        self.assertEqual(cleaned_text, expected_cleaned_text)
w