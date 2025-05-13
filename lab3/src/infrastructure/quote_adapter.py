import requests

from ..application.dto import QuoteFactory
from ..domain.abstractions import IQuoteService


class QuoteApiAdapter(IQuoteService):
    def __init__(self):
        self._url = (
            "http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en"
        )

    def get_random_quote(self):
        try:
            response = requests.get(self._url)
            if response.status_code == 200:
                data = response.json()
                return QuoteFactory.create_quote(data["quoteText"], data["quoteAuthor"])
            else:
                return QuoteFactory.create_quote("No quote available", "Unknown")
        except Exception:
            return QuoteFactory.create_quote("Error fetching quote", "System")
