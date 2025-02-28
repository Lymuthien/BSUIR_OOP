from core import AddFigureCommand, RemoveFigureCommand, MoveFigureCommand, ChangeFigureBgCommand, FileManager, \
    HistoryManager
from models import CanvasModel, CanvasView, DrawableRectangle, DrawableEllipse, DrawableTriangle
from renderers import BasicRenderer, ConsoleCanvasRenderer


class PaintApp(object):
    def __init__(self):
        self.__canvas_model = CanvasModel()
        self.__canvas_view = CanvasView(self.__canvas_model, BasicRenderer())
        self.__history_manager = HistoryManager()

    def render_canvas(self):
        ConsoleCanvasRenderer().render(self.__canvas_view.width, self.__canvas_view.grid)

    def save_file(self, filename: str):
        FileManager.save(self.__canvas_model.get_data, filename)

    def load_file(self, filename: str):
        self.__canvas_model.load_data(FileManager.load(filename))
        self.__canvas_view.update()

    def undo(self):
        self.__history_manager.undo()

    def redo(self):
        self.__history_manager.redo()

    def draw_rectangle(self, x: int, y: int, width: int, height: int):
        self.__history_manager.push_undo_command(
            AddFigureCommand(self.__canvas_model, self.__canvas_view,
                             DrawableRectangle(width, height, 'r'), x, y))

    def draw_triangle(self, x0: int, y0: int, x1: int, y1: int, x2: int, y2: int):
        x_min = min(x0, x1, x2)
        y_min = min(y0, y1, y2)
        self.__history_manager.push_undo_command(
            AddFigureCommand(self.__canvas_model, self.__canvas_view,
                             DrawableTriangle(
                                 ((x0 - x_min, y0 - y_min), (x1 - x_min, y1 - y_min), (x2 - x_min, y2 - y_min)), 't'),
                             x_min, y_min))

    def draw_ellipse(self, x: int, y: int, vertical_r: int, horizontal_r: int):
        self.__history_manager.push_undo_command(
            AddFigureCommand(self.__canvas_model, self.__canvas_view,
                             DrawableEllipse(vertical_r, horizontal_r, 'e'), x, y))

    def select_previous(self):
        self.__canvas_model.navigator.prev()

    def select_next(self):
        self.__canvas_model.navigator.next()

    def remove_figure(self):
        figure = self.__canvas_model.navigator.current()
        self.__history_manager.push_undo_command(
            RemoveFigureCommand(self.__canvas_model, self.__canvas_view, figure))

    def move_figure(self, x: int, y: int):
        figure = self.__canvas_model.navigator.current()
        self.__history_manager.push_undo_command(
            MoveFigureCommand(self.__canvas_model, self.__canvas_view, figure, x, y))

    def change_figure_bg(self, bg: str):
        if len(bg) != 1:
            raise Exception('bg must be 1 character long')
        figure = self.__canvas_model.navigator.current()
        self.__history_manager.push_undo_command(
            ChangeFigureBgCommand(self.__canvas_model, self.__canvas_view, figure, bg))

    def get_figure_info(self) -> dict:
        return self.__canvas_model.get_current_info()
