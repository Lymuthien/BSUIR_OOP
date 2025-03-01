from .core import AddFigureCommand, RemoveFigureCommand, MoveFigureCommand, ChangeFigureBgCommand, FileManager, \
    HistoryManager
from .models import CanvasModel, CanvasView, DrawableRectangle, DrawableEllipse, DrawableTriangle
from .renderers import BasicRenderer, ConsoleCanvasRenderer
from .utils import Navigator


class PaintApp(object):
    def __init__(self):
        self.__canvas_model = CanvasModel(Navigator())
        self.__canvas_view = CanvasView(self.__canvas_model, BasicRenderer())
        self.__history_manager = HistoryManager()
        self.__navigator = Navigator()

    def render_canvas(self):
        """Render the canvas in console."""
        ConsoleCanvasRenderer().render(self.__canvas_view.width, self.__canvas_view.grid)

    def save_file(self, filename: str):
        """Save file by name(path)"""
        FileManager.save(self.__canvas_model.get_data, filename)

    def load_file(self, filename: str):
        """Load file by name(path)"""
        self.__canvas_model.load_data(FileManager.load(filename))
        self.__canvas_view.update()

    def undo(self):
        """Undo last operation"""
        self.__history_manager.undo()

    def redo(self):
        """Redo last operation"""
        self.__history_manager.redo()

    def draw_rectangle(self, x: int, y: int, width: int, height: int):
        """Draw rectangle with given coordinates"""
        self.__history_manager.add_command(
            AddFigureCommand(self.__canvas_model, self.__canvas_view,
                             DrawableRectangle(width, height, 'r'), x, y))

    def draw_triangle(self, x0: int, y0: int, x1: int, y1: int, x2: int, y2: int):
        """Draw triangle with given coordinates"""
        x_min = min(x0, x1, x2)
        y_min = min(y0, y1, y2)
        self.__history_manager.add_command(
            AddFigureCommand(self.__canvas_model, self.__canvas_view,
                             DrawableTriangle(
                                 ((x0 - x_min, y0 - y_min), (x1 - x_min, y1 - y_min), (x2 - x_min, y2 - y_min)), 't'),
                             x_min, y_min))

    def draw_ellipse(self, x: int, y: int, vertical_r: int, horizontal_r: int):
        """Draw ellipse with given coordinates"""
        self.__history_manager.add_command(
            AddFigureCommand(self.__canvas_model, self.__canvas_view,
                             DrawableEllipse(vertical_r, horizontal_r, 'e'), x, y))

    def select_previous(self):
        """Select previous figure"""
        self.__canvas_model.navigator.prev()

    def select_next(self):
        """Select next figure"""
        self.__canvas_model.navigator.next()

    def remove_figure(self):
        """Remove current figure"""
        figure = self.__canvas_model.navigator.current()
        self.__history_manager.add_command(
            RemoveFigureCommand(self.__canvas_model, self.__canvas_view, figure))

    def move_figure(self, x: int, y: int):
        """Move current figure by given coordinates"""
        figure = self.__canvas_model.navigator.current()
        self.__history_manager.add_command(
            MoveFigureCommand(self.__canvas_model, self.__canvas_view, figure, x, y))

    def change_figure_bg(self, bg: str):
        """Change current figure's background color"""
        if len(bg) != 1:
            raise Exception('bg must be 1 character long')
        figure = self.__canvas_model.navigator.current()
        self.__history_manager.add_command(
            ChangeFigureBgCommand(self.__canvas_model, self.__canvas_view, figure, bg))

    def get_figure_info(self) -> dict:
        """Give current figure info"""
        return self.__canvas_model.get_current_info()
