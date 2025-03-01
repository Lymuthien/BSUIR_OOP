from ..interfaces import IRenderer, IDrawable, ICanvasRenderer


class BasicRenderer(IRenderer):
    @staticmethod
    def render(figure: IDrawable, x: int, y: int, grid: list[list[str]]):
        """Render the given drawable figure in the grid by (x, y) coordinates."""
        for r_idx, row in enumerate(figure.render()):
            for s_idx, symbol in enumerate(row):
                if symbol and (0 <= y + r_idx < len(grid)) and (0 <= x + s_idx < len(grid[0])):
                    grid[y + r_idx][x + s_idx] = symbol


class ConsoleCanvasRenderer(ICanvasRenderer):
    @staticmethod
    def render(width: int, grid: tuple[tuple[str, ...], ...]):
        """Render the canvas(grid) in the console."""
        print('-' * width * 2)
        for row in grid:
            print(*row, end='|\n')
        print('-' * width * 2)
