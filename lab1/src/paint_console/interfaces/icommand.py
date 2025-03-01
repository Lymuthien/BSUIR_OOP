from abc import ABC, abstractmethod


class ICommand(ABC):
    @abstractmethod
    def undo(self):
        """Undo action."""
        pass

    @abstractmethod
    def redo(self):
        """Redo action."""
        pass

    @abstractmethod
    def _execute(self):
        pass
