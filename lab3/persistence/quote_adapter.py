import requests
from ..application.dto import QuoteFactory
from ..domain.abstractions import IQuoteGateway


class QuoteApiAdapter(IQuoteGateway):
    def __init__(self):
        self.url = "https://api.quotable.io/random"

    def get_random_quote(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                data = response.json()
                return QuoteFactory.create_quote(data["content"], data["author"])
            else:
                return QuoteFactory.create_quote("No quote available", "Unknown")
        except Exception:
            return QuoteFactory.create_quote("Error fetching quote", "System")
