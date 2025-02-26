from interfaces import IDrawable, ICommand, ICanvasModel, ICanvasView


class AddFigureCommand(ICommand):
    def __init__(self, model: ICanvasModel, view: ICanvasView, figure: IDrawable, x: int, y: int, layer: int = 0):
        self.__model = model
        self.__view = view
        self.__figure = figure
        self.__x = x
        self.__y = y
        self.__layer = layer
        self.__figure_id = None
        self._execute()

    def _execute(self):
        self.__figure_id = self.__model.add_figure(self.__figure, self.__x, self.__y, layer=self.__layer)
        self.__view.draw_figure(self.__figure, self.__x, self.__y)

    def undo(self):
        self.__model.remove_figure(self.__figure_id)
        self.__view.update()

    def redo(self):
        self.__model.add_figure(self.__figure, self.__x, self.__y, layer=self.__layer, figure_id=self.__figure_id)
        self.__view.update()



class RemoveFigureCommand(ICommand):
    def __init__(self, model: ICanvasModel, view: ICanvasView, figure: IDrawable, x: int, y: int, layer: int = 0):
        self.__model = model
        self.__view = view
        self.__figure = figure
        self.__x = x
        self.__y = y
        self.__figure_id = None
        self.__layer = layer
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
    def __init__(self, model: ICanvasModel, view: ICanvasView, figure_id: str, x_old: int, y_old: int,
                 x_new: int, y_new: int):
        self.__model = model
        self.__view = view
        self.__old_coordinates = (x_old, y_old)
        self.__new_coordinates = (x_new, y_new)
        self.__figure_id = figure_id
        self._execute()

    def _execute(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass


class ChangeFigureBgCommand(ICommand):
    def __init__(self):
        pass

    def _execute(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass