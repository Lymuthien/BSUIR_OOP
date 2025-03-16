from abc import ABC, abstractmethod


class ICommand(ABC):
    @abstractmethod
    def undo(self): ...

    @abstractmethod
    def redo(self): ...

    @abstractmethod
    def execute(self): ...
