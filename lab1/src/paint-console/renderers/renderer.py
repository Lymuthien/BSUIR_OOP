from interfaces import IRenderer, IDrawable, ICanvasRenderer


class BasicRenderer(IRenderer):
    @staticmethod
    def render(figure: IDrawable, x: int, y: int, grid: list[list[str]]):
        for r_idx, row in enumerate(figure.render()):
            for s_idx, symbol in enumerate(row):
                if symbol and (0 <= y + r_idx < len(grid)) and (0 <= x + s_idx < len(grid[0])):
                    grid[y + r_idx][x + s_idx] = symbol


class ConsoleCanvasRenderer(ICanvasRenderer):
    @staticmethod
    def render(width: int, grid: tuple[tuple[str, ...], ...]):
        print('-' * width * 2)
        for row in grid:
            print(*row, end='|\n')
        print('-' * width * 2)
