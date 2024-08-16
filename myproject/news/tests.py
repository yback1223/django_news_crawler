from django.test import TestCase
from .gemini_work import GeminiWork

class CleanResponseTextTest(TestCase):
    def setUp(self):
        self.gemini_work = GeminiWork()

    def test_clean_response_text_basic(self):
        # 기본적인 큰따옴표 처리 테스트
        raw_text = 'This is a "test" string.'
        expected_cleaned_text = 'This is a \\"test\\" string.'
        cleaned_text = self.gemini_work.clean_response_text(raw_text)
        self.assertEqual(cleaned_text, expected_cleaned_text)

    def test_clean_response_text_no_quotes(self):
        # 큰따옴표가 없는 경우 테스트
        raw_text = 'This is a test string without quotes.'
        expected_cleaned_text = raw_text  # 변화가 없어야 함
        cleaned_text = self.gemini_work.clean_response_text(raw_text)
        self.assertEqual(cleaned_text, expected_cleaned_text)

    def test_clean_response_text_escaped_quotes(self):
        # 이미 이스케이프된 큰따옴표가 있는 경우 테스트
        raw_text = 'This is a \\"test\\" string.'
        expected_cleaned_text = raw_text  # 변화가 없어야 함
        cleaned_text = self.gemini_work.clean_response_text(raw_text)
        self.assertEqual(cleaned_text, expected_cleaned_text)

    def test_clean_response_text_mixed_quotes(self):
        # 이스케이프되지 않은 큰따옴표와 이스케이프된 큰따옴표가 혼합된 경우 테스트
        raw_text = 'This is a "test\\" string.'
        expected_cleaned_text = 'This is a \\"test\\" string.'
        cleaned_text = self.gemini_work.clean_response_text(raw_text)
        self.assertEqual(cleaned_text, expected_cleaned_text)

    def test_clean_response_text_multiple_quotes(self):
        # 여러 개의 큰따옴표가 있는 경우 테스트
        raw_text = '"First" and "Second" quotes.'
        expected_cleaned_text = '\\"First\\" and \\"Second\\" quotes.'
        cleaned_text = self.gemini_work.clean_response_text(raw_text)
        self.assertEqual(cleaned_text, expected_cleaned_text)
w