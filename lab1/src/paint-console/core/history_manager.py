from interfaces import Command, EventBus


class HistoryManager:
    def __init__(self, event_bus: EventBus):
        self.__event_bus = event_bus
        self.__undo_stack: list[Command] = []
        self.__redo_stack: list[Command] = []
        self.__is_running = False

    def push_undo_command(self, command: Command):
        self.__undo_stack.append(command)
        self.__redo_stack.clear()

    def undo(self):
        if self.__undo_stack and not self.__is_running:
            self.__is_running = True
            command = self.__undo_stack.pop()
            command.undo(self.__event_bus)
            self.__redo_stack.append(command)
            self.__is_running = False

    def redo(self):
        if self.__redo_stack and not self.__is_running:
            self.__is_running = True
            command = self.__redo_stack.pop()
            command.redo(self.__event_bus)
            self.__undo_stack.append(command)
            self.__is_running = False