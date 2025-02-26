from interfaces import ICommand


class HistoryManager:
    def __init__(self):
        self.__undo_stack: list[ICommand] = []
        self.__redo_stack: list[ICommand] = []
        self.__is_running = False

    def push_undo_command(self, command: ICommand):
        self.__undo_stack.append(command)
        self.__redo_stack.clear()

    def undo(self):
        if self.__undo_stack and not self.__is_running:
            self.__is_running = True
            command = self.__undo_stack.pop()
            command.undo()
            self.__redo_stack.append(command)
            self.__is_running = False

    def redo(self):
        if self.__redo_stack and not self.__is_running:
            self.__is_running = True
            command = self.__redo_stack.pop()
            command.redo()
            self.__undo_stack.append(command)
            self.__is_running = False