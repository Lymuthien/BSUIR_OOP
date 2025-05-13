import unittest

from lab3.src.infrastructure.quote_adapter import QuoteApiAdapter


class TestQuoteAdapter(unittest.TestCase):
    def setUp(self):
        self.quote_adapter = QuoteApiAdapter()

    def test_quote_get_random_success(self):
        quote_dto = self.quote_adapter.get_random_quote()

        self.assertIsNotNone(quote_dto.author)
        self.assertIsNotNone(quote_dto.content)
        self.assertTrue(isinstance(quote_dto.author, str))
        self.assertTrue(isinstance(quote_dto.content, str))


if __name__ == "__main__":
    unittest.main()
