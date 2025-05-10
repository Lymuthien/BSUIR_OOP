from abc import ABC, abstractmethod


class IStudent(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def grade(self) -> int: ...

    @property
    @abstractmethod
    def id(self) -> int: ...
