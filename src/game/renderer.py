from typing import Any, Optional
from src.game.enums import CellType
from src.game.grid import Grid
from src.game.position import Position
from src.game.snake import Snake
import curses

"""
For window methods please look at the
https://docs.python.org/3/library/curses.html#window-objects
"""
class Renderer():
    SYMBOL_WALL = "█"
    SYMBOL_BORDER = "░"
    SYMBOL_SNAKE_BODY = 'O'
    SYMBOL_SNAKE_HEAD = 'O'
    SYMBOL_CRASH_SITE = '☒'
    SYMBOL_FOOD = '◉'

    COLOR_PAIR_HEAD_SNAKE = 1
    COLOR_PAIR_FOOD = 2
    COLOR_PAIR_CRASH_SITE = 3

    def __init__(self, window: Any):
        self.window = window
        self._init_curses_colors()

    def _init_curses_colors(self):
        curses.init_pair(self.COLOR_PAIR_HEAD_SNAKE, curses.COLOR_BLUE, -1)
        curses.init_pair(self.COLOR_PAIR_FOOD, curses.COLOR_GREEN, -1)
        curses.init_pair(self.COLOR_PAIR_CRASH_SITE, curses.COLOR_RED, -1)

    def render_level(self, snake: Snake, grid: Grid, food_position: Position):
        self.window.erase()
        subwindow = self._get_grid_subwindow(grid)

        self._draw_borders(subwindow, grid)
        self._draw_grid(subwindow, grid)
        self._draw_snake(subwindow, snake)
        self._draw_food(subwindow, food_position)
        self.window.refresh()
        # self._draw_ui(subwindow, 123)

    def _get_grid_subwindow(self, grid: Grid) -> Any:
        height, width = self.window.getmaxyx()

        grid_width_bordered = grid.width + 2
        grid_height_bordered = grid.height + 2

        offset_x, offset_y = 0, 0
        width_sub_window, height_sub_window = width, height

        if width > grid_width_bordered:
            offset_x = (width - grid_width_bordered) // 2
            width_sub_window = grid_width_bordered

        if height > grid_height_bordered:
            offset_y = (height - grid_height_bordered) // 2
            height_sub_window = grid_height_bordered

        return self.window.subwin(height_sub_window, width_sub_window, offset_y, offset_x)

    def _draw_line_at_with_trimming(self, window, line: str, pos: Position, color_pair_number: Optional[int] = None):
        height, width = window.getmaxyx()
        if height <= pos.y or width <= pos.x:
            return

        line_trimmed = line[:width - pos.x]
        if not line_trimmed:
            return


        arguments = [pos.y, pos.x, line_trimmed]
        if color_pair_number is not None:
            arguments.append(curses.color_pair(color_pair_number))

        # There is a bug is curses implementation.
        # Last line should NOT be drawn with addstr method.
        # https://bugs.python.org/msg218985
        if height - 1 == pos.y:
            window.insstr(*arguments)
        else:
            window.addstr(*arguments)

    def _draw_borders(self, subwindow, grid: Grid):
        border_line_length = grid.width + 2
        border_line = self.SYMBOL_BORDER * border_line_length

        for i in range(0, grid.height + 2):
            self._draw_line_at_with_trimming(subwindow, border_line, Position(0, i))

    def _draw_grid(self, subwindow, grid: Grid):
        for i in range(0, grid.height):
            grid_line = "".join(grid.cells[i]).replace(CellType.WALL.value, self.SYMBOL_WALL)
            self._draw_line_at_with_trimming(subwindow, grid_line, Position(1, i + 1)) # since we have border

    def _draw_snake(self, subwindow, snake: Snake):
        self._draw_line_at_with_trimming(subwindow, self.SYMBOL_SNAKE_HEAD, Position(snake.head_position.x + 1, snake.head_position.y + 1), self.COLOR_PAIR_HEAD_SNAKE)
        for position in snake.positions[1:]:
            self._draw_line_at_with_trimming(subwindow, self.SYMBOL_SNAKE_BODY, Position(position.x + 1, position.y + 1))

    def _draw_food(self, subwindow, food_position: Position):
        self._draw_line_at_with_trimming(subwindow, self.SYMBOL_SNAKE_BODY, Position(food_position.x + 1, food_position.y + 1), self.COLOR_PAIR_FOOD)
