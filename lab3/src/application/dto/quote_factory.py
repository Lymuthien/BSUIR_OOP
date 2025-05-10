from .quote_dto import QuoteDTO


class QuoteFactory:
    @staticmethod
    def create_quote(content: str, author: str) -> QuoteDTO:
        return QuoteDTO(content, author)
