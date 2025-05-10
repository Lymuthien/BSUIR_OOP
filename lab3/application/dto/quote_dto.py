from dataclasses import dataclass


@dataclass
class QuoteDTO:
    content: str
    author: str
