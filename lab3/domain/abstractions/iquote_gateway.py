from abc import ABC, abstractmethod


class IQuoteGateway(ABC):
    @abstractmethod
    def get_random_quote(self): ...
