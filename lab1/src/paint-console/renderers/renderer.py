from ..interfaces import IRenderer, IDrawable


class BasicRenderer(IRenderer):
    def render(self, figure: IDrawable, x: int, y: int, background: str, grid: list[list[str]]):
        for r_idx, row in enumerate(figure.render()):
            for c_idx, symbol in enumerate(row):
                if symbol and (0 <= y + r_idx < len(grid)) and (0 <= x + c_idx < len(grid[0])):
                    grid[y + r_idx][x + c_idx] = symbol