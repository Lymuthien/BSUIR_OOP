from interfaces import IDrawable, ICommand, ICanvasModel, ICanvasView, ISearchingCanvasModel


class AddFigureCommand(ICommand):
    def __init__(self, model: ICanvasModel, view: ICanvasView, figure: IDrawable, x: int, y: int):
        self.__model = model
        self.__view = view
        self.__figure = figure
        self.__x = x
        self.__y = y
        self.__layer = 0
        self.__figure_id = None
        self._execute()

    def _execute(self):
        self.__figure_id = self.__model.add_figure(self.__figure, self.__x, self.__y, layer=self.__layer)
        self.__layer = self.__model.get_figure_layout(self.__figure_id).layer
        self.__view.draw_figure(self.__figure, self.__x, self.__y)

    def undo(self):
        self.__model.remove_figure(self.__figure_id)
        self.__view.update()

    def redo(self):
        self.__model.add_figure(self.__figure, self.__x, self.__y, layer=self.__layer, figure_id=self.__figure_id)
        self.__view.update()



class RemoveFigureCommand(ICommand):
    def __init__(self, model: ISearchingCanvasModel, view: ICanvasView, figure: IDrawable):
        self.__model = model
        self.__view = view
        self.__figure = figure
        self.__figure_id = model.search(figure)
        self.__layer = model.get_figure_layout(self.__figure_id).layer
        self.__x, self.__y = model.get_figure_layout(self.__figure_id).coordinates
        self._execute()

    def _execute(self):
        self.__figure_id = self.__model.remove_figure(self.__figure_id)
        self.__view.update()

    def undo(self):
        self.__model.add_figure(self.__figure, self.__x, self.__y, layer=self.__layer, figure_id=self.__figure_id)
        self.__view.update()

    def redo(self):
        self.__model.remove_figure(self.__figure_id)
        self.__view.update()


class MoveFigureCommand(ICommand):
    def __init__(self, model: ISearchingCanvasModel, view: ICanvasView, figure: IDrawable, x: int, y: int):
        self.__model = model
        self.__view = view
        self.__figure_id = model.search(figure)
        self.__old_coordinates = model.get_figure_layout(self.__figure_id).coordinates
        self.__new_coordinates = (x, y)
        self._execute()

    def _execute(self):
        self.__model.get_figure_layout(self.__figure_id).coordinates = self.__new_coordinates
        self.__view.update()

    def undo(self):
        self.__model.get_figure_layout(self.__figure_id).coordinates = self.__old_coordinates
        self.__view.update()

    def redo(self):
        self.__model.get_figure_layout(self.__figure_id).coordinates = self.__new_coordinates
        self.__view.update()


class ChangeFigureBgCommand(ICommand):
    def __init__(self, model: ISearchingCanvasModel, view: ICanvasView, figure: IDrawable, new_bg: str):
        self.__model = model
        self.__view = view
        self.__figure_id = model.search(figure)
        self.__old_bg = model.get_figure_layout(self.__figure_id).figure.background
        self.__new_bg = new_bg
        self._execute()

    def _execute(self):
        self.__model.get_figure_layout(self.__figure_id).figure.background = self.__new_bg
        self.__view.update()

    def undo(self):
        self.__model.get_figure_layout(self.__figure_id).figure.background = self.__old_bg
        self.__view.update()

    def redo(self):
        self.__model.get_figure_layout(self.__figure_id).figure.background = self.__new_bg
        self.__view.update()


