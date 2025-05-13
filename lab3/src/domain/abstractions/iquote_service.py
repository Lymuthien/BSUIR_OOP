from abc import ABC, abstractmethod


class IQuoteService(ABC):
    @abstractmethod
    def get_random_quote(self): ...
