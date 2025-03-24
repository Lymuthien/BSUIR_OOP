from ..interfaces import ICommand


class HistoryManager:
    def __init__(self):
        self.__undo_stack: list[ICommand] = []
        self.__redo_stack: list[ICommand] = []

    def add_command(self,
                    command: ICommand):
        """Add a command to the stack."""
        self.__undo_stack.append(command)
        self.__redo_stack.clear()

    def undo(self):
        """Undo the last command."""
        if self.__undo_stack:
            command = self.__undo_stack.pop()
            command.undo()
            self.__redo_stack.append(command)
        else:
            raise IndexError("Can't undo (no commands)")

    def redo(self):
        """Redo the last undo command."""
        if self.__redo_stack:
            command = self.__redo_stack.pop()
            command.redo()
            self.__undo_stack.append(command)
        else:
            raise IndexError("Can't redo (no commands)")

    def clear(self):
        self.__undo_stack.clear()
        self.__redo_stack.clear()
