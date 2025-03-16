from abc import abstractmethod, ABC


class IStorageStrategy(ABC):
    @abstractmethod
    def save(self, data, location) -> None: ...

    @abstractmethod
    def load(self, location): ...