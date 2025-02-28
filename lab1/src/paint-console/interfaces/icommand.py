from abc import ABC, abstractmethod


class ICommand(ABC):
    @abstractmethod
    def undo(self):
        pass

    @abstractmethod
    def redo(self):
        pass

    @abstractmethod
    def _execute(self):
        pass
