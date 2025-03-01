from ..interfaces import IRenderer, IDrawable, ICanvasRenderer


class BasicRenderer(IRenderer):
    @staticmethod
    def render(figure: IDrawable, x: int, y: int, grid: list[list[str]]):
        """Render the given drawable figure in the grid by pos(x, y) coordinates."""
        BasicRenderer._validate_coordinates(x, y, grid)

        figure_render = figure.render()
        for r_idx, row in enumerate(figure_render):
            for s_idx, symbol in enumerate(row):
                if symbol and (0 <= y + r_idx < len(grid)) and (0 <= x + s_idx < len(grid[0])):
                    grid[y + r_idx][x + s_idx] = symbol

        BasicRenderer._check_partial_out_of_bounds(figure_render, x, y, grid)

    @staticmethod
    def _validate_coordinates(x: int, y: int, grid: list[list[str]]):
        """Validate initial coordinates before rendering"""
        if x < 0 or y < 0:
            raise ValueError('x and y must be positive')
        if y >= len(grid) or (len(grid) > 0 and x >= len(grid[0])):
            raise IndexError("The given figure in that coordinate is out of bounds of grid.")

    @staticmethod
    def _check_partial_out_of_bounds(figure_render: list[list[str]], x: int, y: int, grid: list[list[str]]):
        """Check for partial out-of-bounds after rendering"""
        if len(figure_render) + y > len(grid) or \
                (len(grid) > 0 and len(figure_render) > 0 and len(figure_render[0]) + x > len(grid[0])):
            raise IndexError("The given figure partly out of bounds of grid.")


# Doesn't need to be tested because it deals with formatted output
class ConsoleCanvasRenderer(ICanvasRenderer):
    @staticmethod
    def render(width: int, grid: tuple[tuple[str, ...], ...]):
        """Render the canvas(grid) in the console."""
        print('-' * width * 2)
        for row in grid:
            print(*row, end='|\n')
        print('-' * width * 2)
