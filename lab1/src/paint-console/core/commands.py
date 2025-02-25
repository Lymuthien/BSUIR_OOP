from interfaces import EventBus, Figure, Command


class AddCommand(Command):
    def __init__(self, figure_id: str, figure: Figure, coordinates: tuple):
        self.__figure_id = figure_id
        self.__figure = figure
        self.__coordinates = coordinates

    def undo(self, event_bus: EventBus):
        event_bus.emit("undo_add", self.__figure_id)

    def redo(self, event_bus: EventBus):
        event_bus.emit("redo_add", self.__figure, self.__coordinates, self.__figure_id)


class RemoveCommand(Command):
    def __init__(self, figure_id: str, figure: Figure, coordinates: tuple):
        self.__figure_id = figure_id
        self.__figure = figure
        self.__coordinates = coordinates

    def undo(self, event_bus: EventBus):
        event_bus.emit("undo_remove", self.__figure, self.__coordinates, self.__figure_id)

    def redo(self, event_bus: EventBus):
        event_bus.emit("redo_remove", self.__figure_id)


class MoveCommand(Command):
    def __init__(self, figure_id: str, old_coordinates: tuple, new_coordinates: tuple):
        self.__figure_id = figure_id
        self.__old_coordinates = old_coordinates
        self.__new_coordinates = new_coordinates

    def undo(self, event_bus: EventBus):
        event_bus.emit("undo_add", self.__figure_id, self.__old_coordinates)

    def redo(self, event_bus: EventBus):
        event_bus.emit("redo_add", self.__figure_id, self.__new_coordinates)


class ChangeBgCommand(Command):
    def __init__(self, figure_id: str, old_bg: str, new_bg: str):
        self.__figure_id = figure_id
        self.__old_bg = old_bg
        self.__new_bg = new_bg

    def undo(self, event_bus: EventBus):
        event_bus.emit("undo_add", self.__figure_id, self.__old_bg)

    def redo(self, event_bus: EventBus):
        event_bus.emit("redo_add", self.__figure_id, self.__new_bg)
